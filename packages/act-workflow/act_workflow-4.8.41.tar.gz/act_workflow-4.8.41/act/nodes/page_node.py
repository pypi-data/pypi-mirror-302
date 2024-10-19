import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PageNode:
    def __init__(self, e2b_sandbox_node, page_name: str):
        self.e2b_sandbox_node = e2b_sandbox_node
        self.page_name = page_name
        self.page_path = f"{self.e2b_sandbox_node.app_dir}/pages/{page_name or 'index'}.tsx"
        self.api_path = f"{self.e2b_sandbox_node.app_dir}/pages/api/{page_name or 'index'}.ts"

    def create(self, page_content: str, api_content: str):
        logger.info(f"Creating page '{self.page_name or 'index'}'")
        self.e2b_sandbox_node.write_file(self.page_path, page_content)
        self.e2b_sandbox_node.write_file(self.api_path, api_content)

    def update(self, page_content: str, api_content: str):
        logger.info(f"Updating page '{self.page_name or 'index'}'")
        self.e2b_sandbox_node.write_file(self.page_path, page_content)
        self.e2b_sandbox_node.write_file(self.api_path, api_content)

    def delete(self):
        logger.info(f"Deleting page '{self.page_name or 'index'}'")
        self.e2b_sandbox_node.sandbox.commands.run(f"rm -f {self.page_path}")
        self.e2b_sandbox_node.sandbox.commands.run(f"rm -f {self.api_path}")


    def generate_page_content(self, content: str, variable_mappings: Dict[str, str]) -> str:
        return f"""
import React from 'react';
import useSWR from 'swr'

const fetcher = (url) => fetch(url).then((res) => res.json());

export default function {self.page_name.capitalize()}Page() {{
    const {{ data, error }} = useSWR('/api/{self.page_name}', fetcher)

    if (error) return <div>Failed to load</div>
    if (!data) return <div>Loading...</div>

    return (
        <div>
            {content}
            <pre>{{JSON.stringify(data, null, 2)}}</pre>
        </div>
    )
}}
"""

    def generate_api_content(self, variable_mappings: Dict[str, str]) -> str:
        return f"""
import {{ NextApiRequest, NextApiResponse }} from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {{
    const variableMappings = {variable_mappings};
    const resolvedVariables = {{}};

    for (const [key, value] of Object.entries(variableMappings)) {{
        resolvedVariables[key] = `Resolved value for ${{value}}`;
    }}

    res.status(200).json(resolvedVariables);
}}
"""

if __name__ == "__main__":
    # This block is for testing the PageNode class independently
    # You would typically not run this directly, but integrate it with your E2BSandboxNode
    from e2b_sandbox_node import E2BSandboxNode

    e2b_sandbox = E2BSandboxNode()
    e2b_sandbox.initialize()

    page_node = PageNode(e2b_sandbox, "test_page")
    page_node.create("<h1>Test Page</h1><p>This is a test page.</p>", {"testVar": "testValue"})

    print(f"Page created. You can view it at {e2b_sandbox.get_public_url()}/test_page")

    # Keep the server running for a while
    import time
    time.sleep(300)

    e2b_sandbox.close()