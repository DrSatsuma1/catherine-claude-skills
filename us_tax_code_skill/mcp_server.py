#!/usr/bin/env python3
"""
MCP Server for US Tax Code
Provides on-demand access to tax code sections via Model Context Protocol
"""

import json
import sys
from pathlib import Path
from typing import Any

# MCP protocol implementation
class TaxCodeMCPServer:
    def __init__(self, skill_dir: Path):
        self.skill_dir = Path(skill_dir)
        self.data_dir = self.skill_dir / "data"

        # Load index
        with open(self.data_dir / "index.json", 'r') as f:
            self.index = json.load(f)

    def get_section(self, section_num: str) -> dict:
        """Get a specific tax code section"""
        if section_num not in self.index["sections"]:
            return {"error": f"Section {section_num} not found"}

        section_info = self.index["sections"][section_num]
        file_path = self.skill_dir / section_info["file"]

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            return {
                "section": section_num,
                "heading": section_info["heading"],
                "content": content
            }
        except Exception as e:
            return {"error": str(e)}

    def search(self, query: str, max_results: int = 10) -> list:
        """Search for sections by keyword"""
        query_lower = query.lower()
        results = []

        # Search in index
        for section_num, section_data in self.index["sections"].items():
            heading_lower = section_data["heading"].lower()
            if query_lower in heading_lower:
                results.append({
                    "section": section_num,
                    "heading": section_data["heading"],
                    "file": section_data["file"]
                })

        return results[:max_results]

    def list_sections(self) -> dict:
        """List all available sections"""
        return {
            "total_sections": len(self.index["sections"]),
            "sections": {
                num: data["heading"]
                for num, data in list(self.index["sections"].items())[:50]
            }
        }

    def handle_request(self, method: str, params: dict) -> dict:
        """Handle MCP requests"""
        if method == "get_section":
            return self.get_section(params.get("section_num"))
        elif method == "search":
            return self.search(params.get("query"), params.get("max_results", 10))
        elif method == "list_sections":
            return self.list_sections()
        else:
            return {"error": f"Unknown method: {method}"}


def main():
    # Get skill directory
    skill_dir = Path(__file__).parent
    server = TaxCodeMCPServer(skill_dir)

    print(json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "name": "us-tax-code",
            "version": "1.0.0",
            "description": "US Internal Revenue Code access via MCP",
            "methods": [
                "get_section",
                "search",
                "list_sections"
            ]
        }
    }))


if __name__ == "__main__":
    main()
