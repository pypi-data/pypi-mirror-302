from e2b_sandbox_node import E2BSandboxNode
from page_node import PageNode
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize the E2B Sandbox
e2b_sandbox = E2BSandboxNode()
e2b_sandbox.initialize()

# List to keep track of all pages
pages = []

# Function to create a new page
def create_page(name, title, page_content, api_content):
    page = PageNode(e2b_sandbox, name)
    page.create(page_content, api_content)
    pages.append({"name": name, "title": title})
    print(f"Created page: {e2b_sandbox.get_public_url()}/{name}")

# Create home page with menu
def create_home_page():
    menu_items = "".join([f'<li><a href="/{page["name"]}">{page["title"]}</a></li>' for page in pages])
    home_page_content = f"""
import React from 'react';

export default function HomePage() {{
    return (
        <div>
            <h1>Welcome to Our Next.js Site</h1>
            <nav>
                <ul>
                    {menu_items}
                </ul>
            </nav>
        </div>
    );
}}
"""
    home_api_content = """
import { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    res.status(200).json({ message: "Welcome to the home page API" });
}
"""
    home_page = PageNode(e2b_sandbox, "")  # Empty string for root path
    home_page.create(home_page_content, home_api_content)
    print(f"Created home page: {e2b_sandbox.get_public_url()}")

# Create pages
create_page("about", "About Us", 
"""
import React from 'react';
import Link from 'next/link';

export default function AboutPage() {
    return (
        <div>
            <h1>About Us</h1>
            <p>This is the about page.</p>
            <Link href="/">Back to Home</Link>
        </div>
    );
}
""",
"""
import { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    res.status(200).json({ company: "Our Company" });
}
""")

create_page("contact", "Contact Us", 
"""
import React from 'react';
import Link from 'next/link';

export default function ContactPage() {
    return (
        <div>
            <h1>Contact Us</h1>
            <p>Get in touch with us here.</p>
            <Link href="/">Back to Home</Link>
        </div>
    );
}
""",
"""
import { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    res.status(200).json({ email: "contact@example.com" });
}
""")

create_page("services", "Our Services", 
"""
import React from 'react';
import Link from 'next/link';

export default function ServicesPage() {
    return (
        <div>
            <h1>Our Services</h1>
            <ul>
                <li>Service 1</li>
                <li>Service 2</li>
            </ul>
            <Link href="/">Back to Home</Link>
        </div>
    );
}
""",
"""
import { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    res.status(200).json({ services: ["Service 1", "Service 2"] });
}
""")

# Create home page with menu after other pages are created
create_home_page()

print(f"\nE2B Sandbox Node initialized. Public URL: {e2b_sandbox.get_public_url()}")
print("You can now access the following pages:")
print(f"- Home: {e2b_sandbox.get_public_url()}")
for page in pages:
    print(f"- {page['title']}: {e2b_sandbox.get_public_url()}/{page['name']}")

# Keep the server running for a while
print("\nThe app will run for 10 minutes. You can open it in your browser.")
time.sleep(600)

e2b_sandbox.close()