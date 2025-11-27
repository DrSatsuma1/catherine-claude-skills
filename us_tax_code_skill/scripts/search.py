#!/usr/bin/env python3
"""Tax Code Search Functionality"""

import json
import re
from pathlib import Path
from typing import List, Dict

class TaxCodeSearch:
    def __init__(self, skill_dir: Path):
        self.skill_dir = Path(skill_dir)
        self.data_dir = self.skill_dir / "data"
        
        # Load index
        with open(self.data_dir / "index.json", 'r') as f:
            self.index = json.load(f)
    
    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search for sections by keyword"""
        query_words = set(re.findall(r'\b[a-z]+\b', query.lower()))
        
        # Score sections based on word matches
        scores = {}
        
        # Check search index
        for word in query_words:
            if word in self.index.get("search_index", {}):
                for section_num in self.index["search_index"][word]:
                    scores[section_num] = scores.get(section_num, 0) + 1
        
        # Check section headings
        for section_num, section_data in self.index.get("sections", {}).items():
            heading_words = set(re.findall(r'\b[a-z]+\b', section_data["heading"].lower()))
            match_count = len(query_words & heading_words)
            if match_count > 0:
                scores[section_num] = scores.get(section_num, 0) + (match_count * 2)
        
        # Sort by score
        results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_results]
        
        # Return section data
        return [
            {
                "section": section_num,
                "heading": self.index["sections"][section_num]["heading"],
                "file": self.index["sections"][section_num]["file"],
                "score": score
            }
            for section_num, score in results
        ]
    
    def load_section(self, section_num: str) -> str:
        """Load a specific section"""
        if section_num in self.index.get("sections", {}):
            file_path = self.data_dir.parent / self.index["sections"][section_num]["file"]
            with open(file_path, 'r') as f:
                return f.read()
        return None
    
    def get_cross_references(self, section_num: str) -> List[str]:
        """Get sections referenced by this section"""
        content = self.load_section(section_num)
        if content:
            refs = re.findall(r'section\s+(\d+[A-Za-z]?)', content, re.IGNORECASE)
            return list(set(refs))
        return []

def search_tax_code(query: str, skill_dir: str = ".") -> List[Dict]:
    """Main search function"""
    searcher = TaxCodeSearch(skill_dir)
    return searcher.search(query)

def load_section(section_num: str, skill_dir: str = ".") -> str:
    """Load a specific section"""
    searcher = TaxCodeSearch(skill_dir)
    return searcher.load_section(section_num)
