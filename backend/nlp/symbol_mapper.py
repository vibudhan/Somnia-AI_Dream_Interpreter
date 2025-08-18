"""
Symbol Mapper - Maps extracted dream symbols to psychological meanings
Uses curated symbolic dictionary and cultural interpretation frameworks
"""

import json
import os
from typing import List, Dict, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SymbolMapper:
    """
    Maps dream symbols to their psychological and cultural meanings
    """
    
    def __init__(self, symbols_file_path: str = None):
        """Initialize with symbol dictionary"""
        if symbols_file_path is None:
            symbols_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'symbols.json')
        
        self.symbols_dict = self._load_symbols_dictionary(symbols_file_path)
        self.cultural_contexts = self._load_cultural_contexts()
        
    def _load_symbols_dictionary(self, file_path: str) -> Dict:
        """Load the symbolic dictionary from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Symbols dictionary not found at {file_path}, using default symbols")
            return self._get_default_symbols()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing symbols dictionary: {e}")
            return self._get_default_symbols()

    def _get_default_symbols(self) -> Dict:
        """Default symbolic dictionary for fallback"""
        return {
            "animals": {
                "dog": {
                    "meanings": ["loyalty", "friendship", "protection", "instinct"],
                    "psychological": "Represents faithful relationships and protective instincts",
                    "cultural_variants": {
                        "western": "companion and loyalty",
                        "eastern": "fortune and prosperity"
                    }
                },
                "snake": {
                    "meanings": ["transformation", "healing", "wisdom", "danger"],
                    "psychological": "Represents transformation, hidden knowledge, or repressed fears",
                    "cultural_variants": {
                        "western": "temptation or medicine",
                        "eastern": "wisdom and renewal"
                    }
                },
                "bird": {
                    "meanings": ["freedom", "spirituality", "messages", "perspective"],
                    "psychological": "Represents desire for freedom, spiritual aspirations, or higher perspective",
                    "cultural_variants": {
                        "universal": "freedom and transcendence"
                    }
                }
            },
            "water": {
                "ocean": {
                    "meanings": ["unconscious", "emotions", "vastness", "unknown"],
                    "psychological": "Represents the vast unconscious mind and deep emotions",
                    "cultural_variants": {
                        "universal": "life source and mystery"
                    }
                },
                "river": {
                    "meanings": ["life flow", "time", "journey", "change"],
                    "psychological": "Represents the flow of life and personal journey",
                    "cultural_variants": {
                        "universal": "life passage and renewal"
                    }
                }
            },
            "flight": {
                "flying": {
                    "meanings": ["freedom", "transcendence", "escape", "spiritual elevation"],
                    "psychological": "Represents desire for freedom from limitations or spiritual growth",
                    "cultural_variants": {
                        "universal": "liberation and aspiration"
                    }
                },
                "falling": {
                    "meanings": ["loss of control", "anxiety", "failure", "letting go"],
                    "psychological": "Represents fear of failure or losing control in waking life",
                    "cultural_variants": {
                        "western": "anxiety and loss of control",
                        "eastern": "letting go and surrender"
                    }
                }
            },
            "people": {
                "stranger": {
                    "meanings": ["unknown aspects of self", "new opportunities", "fear of unknown"],
                    "psychological": "May represent unknown aspects of personality or new life possibilities",
                    "cultural_variants": {
                        "universal": "the unknown self or other"
                    }
                }
            },
            "objects": {
                "mirror": {
                    "meanings": ["self-reflection", "truth", "vanity", "introspection"],
                    "psychological": "Represents self-examination and truth about oneself",
                    "cultural_variants": {
                        "western": "self-reflection and vanity",
                        "eastern": "illusion and reality"
                    }
                },
                "key": {
                    "meanings": ["solutions", "access", "secrets", "opportunity"],
                    "psychological": "Represents access to hidden knowledge or solutions to problems",
                    "cultural_variants": {
                        "universal": "access and solutions"
                    }
                }
            }
        }

    def _load_cultural_contexts(self) -> Dict:
        """Load cultural interpretation contexts"""
        return {
            "western": {
                "emphasis": ["individual psychology", "personal growth", "psychological healing"],
                "frameworks": ["Freudian", "Jungian", "Gestalt"]
            },
            "eastern": {
                "emphasis": ["spiritual growth", "harmony", "collective wisdom"],
                "frameworks": ["Buddhist", "Taoist", "Hindu"]
            },
            "indigenous": {
                "emphasis": ["nature connection", "spiritual guidance", "community wisdom"],
                "frameworks": ["shamanic", "animistic"]
            }
        }

    def map_symbols(self, extracted_symbols: List[Dict]) -> List[Dict]:
        """
        Map extracted symbols to their psychological meanings
        """
        mapped_symbols = []
        
        for symbol_data in extracted_symbols:
            symbol_name = symbol_data.get('symbol', '').lower()
            category = symbol_data.get('category', 'unknown')
            confidence = symbol_data.get('confidence', 0.5)
            
            # Find symbol meaning
            meaning_data = self._find_symbol_meaning(symbol_name, category)
            
            if meaning_data:
                mapped_symbol = {
                    'symbol': symbol_data.get('symbol', '').title(),
                    'category': category,
                    'meaning': meaning_data.get('psychological', 'Unknown meaning'),
                    'keywords': meaning_data.get('meanings', []),
                    'confidence': confidence,
                    'cultural_meanings': meaning_data.get('cultural_variants', {}),
                    'context': symbol_data.get('context', '')
                }
                mapped_symbols.append(mapped_symbol)
        
        return self._rank_symbols(mapped_symbols)

    def _find_symbol_meaning(self, symbol_name: str, category: str) -> Optional[Dict]:
        """Find meaning for a specific symbol"""
        
        # First try to find in the specific category
        if category in self.symbols_dict:
            category_symbols = self.symbols_dict[category]
            if symbol_name in category_symbols:
                return category_symbols[symbol_name]
        
        # If not found, search across all categories
        for cat_name, cat_symbols in self.symbols_dict.items():
            if symbol_name in cat_symbols:
                return cat_symbols[symbol_name]
        
        # If still not found, try partial matches
        for cat_name, cat_symbols in self.symbols_dict.items():
            for sym_name, sym_data in cat_symbols.items():
                if symbol_name in sym_name or sym_name in symbol_name:
                    return sym_data
        
        return None

    def _rank_symbols(self, symbols: List[Dict]) -> List[Dict]:
        """Rank symbols by importance and confidence"""
        
        # Weight factors for ranking
        category_weights = {
            'animals': 1.2,
            'water': 1.1,
            'flight': 1.3,
            'people': 1.0,
            'objects': 0.9,
            'places': 0.8,
            'abstract': 1.1
        }
        
        for symbol in symbols:
            category = symbol.get('category', 'unknown')
            base_confidence = symbol.get('confidence', 0.5)
            
            # Apply category weighting
            category_weight = category_weights.get(category, 1.0)
            
            # Calculate final ranking score
            symbol['ranking_score'] = base_confidence * category_weight
        
        # Sort by ranking score (highest first)
        return sorted(symbols, key=lambda x: x.get('ranking_score', 0), reverse=True)

    def get_symbol_relationships(self, symbols: List[str]) -> Dict:
        """
        Find relationships and patterns between symbols
        """
        relationships = {
            'complementary': [],
            'conflicting': [],
            'thematic_groups': []
        }
        
        # Define symbol relationships
        complementary_pairs = [
            ('water', 'flying'),
            ('key', 'door'),
            ('light', 'dark'),
            ('birth', 'death')
        ]
        
        conflicting_pairs = [
            ('flying', 'falling'),
            ('found', 'lost'),
            ('safe', 'danger')
        ]
        
        # Check for complementary relationships
        for symbol1, symbol2 in complementary_pairs:
            if symbol1 in symbols and symbol2 in symbols:
                relationships['complementary'].append((symbol1, symbol2))
        
        # Check for conflicting relationships
        for symbol1, symbol2 in conflicting_pairs:
            if symbol1 in symbols and symbol2 in symbols:
                relationships['conflicting'].append((symbol1, symbol2))
        
        # Group by themes
        theme_groups = {
            'transformation': ['snake', 'butterfly', 'fire', 'death', 'birth'],
            'journey': ['path', 'road', 'bridge', 'car', 'walking'],
            'relationships': ['family', 'friend', 'lover', 'stranger', 'teacher'],
            'nature': ['tree', 'mountain', 'ocean', 'forest', 'bird', 'animal']
        }
        
        for theme, theme_symbols in theme_groups.items():
            matching_symbols = [s for s in symbols if s.lower() in theme_symbols]
            if len(matching_symbols) >= 2:
                relationships['thematic_groups'].append({
                    'theme': theme,
                    'symbols': matching_symbols
                })
        
        return relationships

    def get_archetypal_meanings(self, symbols: List[str]) -> List[Dict]:
        """
        Map symbols to Jungian archetypal meanings
        """
        archetypal_mappings = {
            'hero': ['sword', 'quest', 'battle', 'victory', 'rescue'],
            'shadow': ['monster', 'demon', 'dark', 'hidden', 'evil'],
            'anima': ['wise_woman', 'beautiful_woman', 'guide', 'inspiration'],
            'animus': ['wise_man', 'strong_man', 'father_figure', 'authority'],
            'mother': ['nurturing', 'protection', 'home', 'food', 'care'],
            'child': ['innocence', 'wonder', 'playfulness', 'potential', 'new_beginning'],
            'trickster': ['fool', 'joker', 'mischief', 'chaos', 'humor'],
            'sage': ['wise_old_man', 'teacher', 'book', 'wisdom', 'knowledge']
        }
        
        archetypal_symbols = []
        
        for archetype, archetype_symbols in archetypal_mappings.items():
            matching_symbols = [s for s in symbols if s.lower() in archetype_symbols]
            if matching_symbols:
                archetypal_symbols.append({
                    'archetype': archetype,
                    'symbols': matching_symbols,
                    'meaning': self._get_archetypal_meaning(archetype)
                })
        
        return archetypal_symbols

    def _get_archetypal_meaning(self, archetype: str) -> str:
        """Get meaning for specific archetype"""
        meanings = {
            'hero': 'Represents the drive to overcome challenges and achieve goals',
            'shadow': 'Represents repressed or denied aspects of the self',
            'anima': 'Represents the feminine aspect of the male psyche',
            'animus': 'Represents the masculine aspect of the female psyche',
            'mother': 'Represents nurturing, protection, and unconditional love',
            'child': 'Represents innocence, potential, and new beginnings',
            'trickster': 'Represents the need for humor and flexibility',
            'sage': 'Represents wisdom, knowledge, and spiritual guidance'
        }
        
        return meanings.get(archetype, 'Unknown archetypal meaning')

    def add_custom_symbol(self, symbol: str, category: str, meanings: List[str], 
                         psychological_meaning: str, cultural_variants: Dict = None):
        """
        Add a custom symbol to the dictionary
        """
        if category not in self.symbols_dict:
            self.symbols_dict[category] = {}
        
        self.symbols_dict[category][symbol.lower()] = {
            'meanings': meanings,
            'psychological': psychological_meaning,
            'cultural_variants': cultural_variants or {}
        }
        
        logger.info(f"Added custom symbol: {symbol} to category: {category}")

    def save_symbols_dictionary(self, file_path: str):
        """Save the current symbols dictionary to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.symbols_dict, f, indent=2, ensure_ascii=False)
            logger.info(f"Symbols dictionary saved to: {file_path}")
        except Exception as e:
            logger.error(f"Failed to save symbols dictionary: {e}")