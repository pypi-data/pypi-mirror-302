import json
import logging
import time
import threading
import requests
from typing import Dict, Any
from e2b_code_interpreter import Sandbox

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class E2BSandboxNode:
    def __init__(self):
        self.sandbox = None
        self.app_dir = "app"
        self.public_url = None
        self.nextjs_process = None
        self.server_ready = False

    def initialize(self):
        logger.info("Initializing E2B Sandbox for Next.js 15")
        self.sandbox = Sandbox()
        self.setup_nextjs_app()
        self.start_nextjs_server()

    def setup_nextjs_app(self):
        logger.info("Setting up Next.js 15 app")
        self.create_directory(f"{self.app_dir}/pages")
        self.create_directory(f"{self.app_dir}/pages/api")
        self.create_directory(f"{self.app_dir}/styles")

        # Create package.json
        package_json = {
            "name": "nextjs-15-workflow-ui",
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": {
                "next": "^13.4.4",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@types/node": "^20.0.0",
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "typescript": "^5.0.0",
                "swr": "^2.0.0"
            }
        }
        self.write_file(f"{self.app_dir}/package.json", json.dumps(package_json, indent=2))

        # Create tsconfig.json
        tsconfig_json = {
            "compilerOptions": {
                "target": "es5",
                "lib": ["dom", "dom.iterable", "esnext"],
                "allowJs": True,
                "skipLibCheck": True,
                "strict": True,
                "noEmit": True,
                "esModuleInterop": True,
                "module": "esnext",
                "moduleResolution": "bundler",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "jsx": "preserve",
                "incremental": True,
                "plugins": [
                    {
                        "name": "next"
                    }
                ],
                "paths": {
                    "@/*": ["./*"]
                }
            },
            "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
            "exclude": ["node_modules"]
        }
        self.write_file(f"{self.app_dir}/tsconfig.json", json.dumps(tsconfig_json, indent=2))

        # Create next.config.js
        next_config = """
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
}

module.exports = nextConfig
"""
        self.write_file(f"{self.app_dir}/next.config.js", next_config)

        # Create _app.tsx
        app_content = """
import '../styles/globals.css'
import type { AppProps } from 'next/app'

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}

export default MyApp
"""
        self.write_file(f"{self.app_dir}/pages/_app.tsx", app_content)

        # Create globals.css
        globals_css = """
html,
body {
  padding: 0;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen,
    Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
}

a {
  color: inherit;
  text-decoration: none;
}

* {
  box-sizing: border-box;
}
"""
        self.write_file(f"{self.app_dir}/styles/globals.css", globals_css)

        # Create index.tsx (home page)
        index_page_content = """
import React from 'react';

export default function Home() {
    return (
        <div>
            <h1>Welcome to the E2B Sandbox Next.js App</h1>
            <p>This is the default home page.</p>
        </div>
    );
}
"""
        self.write_file(f"{self.app_dir}/pages/index.tsx", index_page_content)

        logger.info("Next.js 15 app setup completed")

        # Install dependencies
        logger.info("Installing dependencies...")
        result = self.sandbox.commands.run("npm install", cwd=self.app_dir)
        logger.info(f"Dependencies installed. Result: {result}")

    def start_nextjs_server(self):
        logger.info("Starting Next.js development server...")
        try:
            self.nextjs_process = self.sandbox.commands.run(
                "npm run dev -- -p 3000",
                cwd=self.app_dir,
                background=True
            )
            logger.info("Next.js development server process started.")

            # Start a thread to capture the output
            threading.Thread(target=self.capture_nextjs_output, daemon=True).start()

            # Get the public URL
            host = self.sandbox.get_host(3000)
            self.public_url = f"https://{host}"
            logger.info(f"Next.js app should be accessible at {self.public_url}")

            # Wait for the server to be accessible
            max_wait_time = 60  # Maximum wait time in seconds
            start_time = time.time()
            while not self.is_server_accessible():
                if time.time() - start_time > max_wait_time:
                    logger.error("Timeout waiting for Next.js server to be accessible")
                    raise Exception("Next.js server failed to become accessible within the expected time")
                time.sleep(1)

            logger.info(f"Next.js app is now accessible at {self.public_url}")

        except Exception as e:
            logger.error(f"Failed to start Next.js server: {e}")
            raise

    def capture_nextjs_output(self):
        for stdout, stderr, _ in self.nextjs_process:
            if stdout:
                logger.info(f"Next.js stdout: {stdout.strip()}")
                if "ready - started server on" in stdout:
                    self.server_ready = True
            if stderr:
                logger.error(f"Next.js stderr: {stderr.strip()}")

    def is_server_accessible(self):
        try:
            response = requests.get(self.public_url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def create_directory(self, path: str):
        self.sandbox.commands.run(f"mkdir -p {path}")

    def write_file(self, path: str, content: str):
        # Ensure the directory exists before writing the file
        dir_path = path.rsplit('/', 1)[0]
        self.create_directory(dir_path)
        command = f"cat << 'EOF' > {path}\n{content}\nEOF"
        self.sandbox.commands.run(command)

    def get_sandbox(self):
        return self.sandbox

    def get_public_url(self):
        return self.public_url

    def close(self):
        if self.nextjs_process:
            self.nextjs_process.kill()
            logger.info("Next.js server process terminated.")
        if self.sandbox:
            self.sandbox = None
            logger.info("Sandbox shutdown completed")

if __name__ == "__main__":
    # This block is for testing the E2BSandboxNode class independently
    e2b_sandbox = E2BSandboxNode()
    e2b_sandbox.initialize()
    
    print(f"E2B Sandbox Node initialized. Public URL: {e2b_sandbox.get_public_url()}")
    
    # Keep the server running for a while
    print("The app will run for 5 minutes. You can open it in your browser.")
    time.sleep(300)
    
    e2b_sandbox.close()