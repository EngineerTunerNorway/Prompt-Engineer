#
# Prompt Engineer v1.0 Made by xeQter 2025.
#
# This is a work in progress. So expect bugs.
#
# You have to make your own list woth saved prompts. Mine is private.

import sys
import json
import uuid
import random
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional, Any
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QComboBox, QLabel, QSplitter, QTabWidget, QMenuBar, QToolBar,
    QStatusBar, QMessageBox, QDialog, QDialogButtonBox, QFormLayout,
    QGroupBox, QCheckBox, QSpinBox, QFileDialog, QProgressBar,
    QTreeWidget, QTreeWidgetItem, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QObject
from PyQt6.QtGui import QAction, QFont, QTextCharFormat, QSyntaxHighlighter


@dataclass
class Prompt:
    id: str
    title: str
    content: str
    platform: str
    category: str
    created_at: str
    modified_at: str
    usage_count: int = 0
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class EnhancementLibrary:
    def __init__(self):
        self.style_modifiers = [
            # Visual Quality Terms
            "Hyper Realistic", "Photorealistic", "Ultra Detailed", "High Resolution",
            "Cinematic", "Dramatic Lighting", "Professional Quality", "Studio Grade",
            "Masterpiece", "Award Winning", "Stunning", "Breathtaking", "Exceptional",
            "Premium", "Luxury", "Elegant", "Sophisticated", "Refined", "Polished",
            "Ultra-Realistic", "Macro Details", "Ultra Sharp", "Vivid Colors",
            "Noir", "Moody Atmosphere", "High Contrast", "Cinematic Scope",
            "Epic Scale", "Photojournalistic", "Surreal Vignettes", "Dreamlike",
            "Minimalist", "Maximalist", "Ethereal Glow", "Volumetric Light",
            "Lens Flare", "Tilt-Shift Effect", "Depth of Field", "HDR",
            
            # Advanced Visual Terms
            "8K Resolution", "Ultra-High Definition", "Crystal Clear", "Razor Sharp",
            "Museum Quality", "Gallery Standard", "Exhibition Grade", "Archival Quality",
            "Pristine Condition", "Flawless Execution", "Immaculate Detail", "Perfect Clarity",
            "Sublime Beauty", "Transcendent Quality", "Divine Craftsmanship", "Legendary Status",
            "Iconic Composition", "Timeless Appeal", "Universal Excellence", "Paradigm-Shifting",
            "Revolutionary Aesthetics", "Groundbreaking Visuals", "Next-Generation Quality",
            "State-of-the-Art", "Cutting-Edge Precision", "Unprecedented Detail",
            
            # Atmospheric and Mood Terms
            "Atmospheric Perspective", "Golden Hour Lighting", "Blue Hour Ambiance",
            "Chiaroscuro Effect", "Rim Lighting", "Backlighting", "Side Lighting",
            "Ambient Occlusion", "Global Illumination", "Ray Traced Reflections",
            "Subsurface Scattering", "Volumetric Fog", "Particle Effects",
            "Motion Blur", "Bokeh Effect", "Film Grain", "Color Grading",
            "LUT Applied", "Tone Mapping", "Exposure Bracketing"
        ]
        
        self.technical_terms = [
            # Core Technology
            "Machine Learning", "Neural Network", "Deep Learning", "Algorithm",
            "Data Science", "Analytics", "Optimization", "Performance Tuning",
            "Scalability", "Architecture", "Framework", "Implementation",
            "Methodology", "Best Practices", "Industry Standard", "Enterprise Grade",
            "API Integration", "Real-time Processing", "Latency Reduction",
            "Parallel Computing", "Concurrency", "Thread Safety", "Memory Management",
            "Profiling", "Benchmarking", "Data Pipeline", "CI/CD", "Containerization",
            "Virtualization", "Microservices", "Edge Computing", "Cloud-Native",
            "Distributed Systems", "Fault Tolerance", "High Availability",
            
            # Advanced AI/ML Terms
            "Transformer Architecture", "Attention Mechanism", "Gradient Descent",
            "Backpropagation", "Reinforcement Learning", "Supervised Learning",
            "Unsupervised Learning", "Semi-Supervised Learning", "Transfer Learning",
            "Few-Shot Learning", "Zero-Shot Learning", "Meta-Learning",
            "Federated Learning", "Adversarial Training", "Generative AI",
            "Large Language Model", "Foundation Model", "Multimodal AI",
            "Computer Vision", "Natural Language Processing", "Speech Recognition",
            "Anomaly Detection", "Predictive Analytics", "Time Series Analysis",
            
            # Software Engineering Excellence
            "Code Quality", "Technical Debt", "Refactoring", "Design Patterns",
            "SOLID Principles", "Clean Code", "Test-Driven Development",
            "Behavior-Driven Development", "Domain-Driven Design", "Event Sourcing",
            "CQRS Pattern", "Hexagonal Architecture", "Onion Architecture",
            "Repository Pattern", "Factory Pattern", "Observer Pattern",
            "Dependency Injection", "Inversion of Control", "Aspect-Oriented Programming"
        ]
        
        self.creative_terms = [
            # Original Creative Terms
            "Innovative", "Creative", "Original", "Unique", "Artistic", "Imaginative",
            "Visionary", "Cutting Edge", "Revolutionary", "Groundbreaking",
            "Trendsetting", "Pioneering", "Advanced", "Progressive", "Modern",
            "Whimsical", "Surreal", "Fantasy", "Abstract", "Ethereal",
            "Futuristic", "Retro", "Steampunk", "Cyberpunk", "Bohemian",
            "Quirky", "Playful", "Edgy", "Avant-Garde", "Dreamlike",
            "Organic", "Fluid", "Kinetic",
            
            # Expanded Creative Expressions
            "Transcendent", "Mystical", "Enchanting", "Mesmerizing", "Captivating",
            "Spellbinding", "Hypnotic", "Otherworldly", "Supernatural", "Magical",
            "Fantastical", "Mythical", "Legendary", "Epic", "Heroic",
            "Dramatic", "Theatrical", "Cinematic", "Operatic", "Symphonic",
            "Poetic", "Lyrical", "Rhythmic", "Harmonic", "Melodic",
            "Expressive", "Emotive", "Passionate", "Intense", "Powerful",
            "Dynamic", "Energetic", "Vibrant", "Electric", "Magnetic",
            "Radiant", "Luminous", "Brilliant", "Dazzling", "Spectacular",
            
            # Artistic Movements and Styles
            "Impressionistic", "Expressionistic", "Cubist", "Surrealist", "Dadaist",
            "Minimalist", "Maximalist", "Brutalist", "Art Nouveau", "Art Deco",
            "Bauhaus", "Gothic", "Renaissance", "Baroque", "Rococo",
            "Neoclassical", "Romantic", "Contemporary", "Postmodern", "Deconstructivist"
        ]
        
        # New category: Reasoning and Logic Frameworks
        self.reasoning_frameworks = [
            "Chain of Thought", "Tree of Thoughts", "Step-by-Step Analysis",
            "Logical Deduction", "Inductive Reasoning", "Abductive Reasoning",
            "Causal Analysis", "Root Cause Analysis", "Systems Thinking",
            "Critical Thinking", "Analytical Framework", "Structured Problem Solving",
            "Decision Matrix", "SWOT Analysis", "Risk Assessment",
            "Cost-Benefit Analysis", "Comparative Analysis", "Scenario Planning",
            "Hypothesis Testing", "Scientific Method", "Experimental Design",
            "Statistical Analysis", "Data-Driven Insights", "Evidence-Based Reasoning",
            "First Principles Thinking", "Reverse Engineering", "Decomposition Method",
            "Synthesis Approach", "Holistic Perspective", "Multi-Dimensional Analysis"
        ]
        
        # New category: Output Formatting and Structure
        self.output_formatting = [
            "Structured Response", "Bulleted List", "Numbered Steps", "Hierarchical Format",
            "Table Format", "JSON Structure", "XML Format", "Markdown Syntax",
            "Executive Summary", "Detailed Breakdown", "Concise Overview", "Comprehensive Report",
            "Action Items", "Key Takeaways", "Summary Points", "Conclusion Statement",
            "Recommendations", "Next Steps", "Implementation Plan", "Timeline Format",
            "Progress Tracking", "Milestone Markers", "Phase-by-Phase", "Categorical Organization",
            "Prioritized List", "Ranked Order", "Chronological Sequence", "Logical Flow",
            "Visual Diagram", "Flowchart Format", "Mind Map Structure", "Comparison Chart"
        ]
        
        # New category: Tone and Voice Modifiers
        self.tone_voice = [
            "Professional", "Conversational", "Technical", "Academic", "Business Formal",
            "Friendly", "Authoritative", "Collaborative", "Instructional", "Explanatory",
            "Persuasive", "Informative", "Analytical", "Creative", "Inspiring",
            "Motivational", "Empathetic", "Diplomatic", "Direct", "Concise",
            "Detailed", "Comprehensive", "Simplified", "Advanced", "Beginner-Friendly",
            "Expert-Level", "Consultative", "Advisory", "Mentoring", "Coaching",
            "Objective", "Subjective", "Neutral", "Opinionated", "Balanced",
            "Cautious", "Confident", "Optimistic", "Realistic", "Pragmatic",
            "Strategic", "Tactical", "Operational", "Executive", "Managerial"
        ]
        
        # New category: Quality and Precision Modifiers
        self.quality_precision = [
            "Precise", "Accurate", "Exact", "Specific", "Detailed", "Thorough",
            "Comprehensive", "Complete", "Exhaustive", "In-Depth", "Granular",
            "Meticulous", "Rigorous", "Systematic", "Methodical", "Structured",
            "Organized", "Logical", "Coherent", "Consistent", "Reliable",
            "Validated", "Verified", "Tested", "Proven", "Evidence-Based",
            "Research-Backed", "Data-Driven", "Fact-Checked", "Peer-Reviewed",
            "Industry-Validated", "Best-Practice", "Standard-Compliant",
            "Quality-Assured", "Performance-Optimized", "Efficiency-Focused"
        ]
        
        # New category: Industry-Specific Terms
        self.industry_terms = {
            "Healthcare": [
                "Clinical Excellence", "Patient-Centered", "Evidence-Based Medicine",
                "Healthcare Innovation", "Medical Best Practices", "Regulatory Compliance",
                "HIPAA Compliant", "FDA Approved", "Clinical Trial", "Peer-Reviewed"
            ],
            "Finance": [
                "Risk Management", "Regulatory Compliance", "Financial Modeling",
                "Portfolio Optimization", "Due Diligence", "Audit Trail",
                "SOX Compliance", "Basel III", "Stress Testing", "Quantitative Analysis"
            ],
            "Technology": [
                "Digital Transformation", "Innovation Pipeline", "Agile Methodology",
                "DevOps Culture", "Cloud-First", "API-First", "Mobile-First",
                "Security-by-Design", "Privacy-by-Design", "Scalable Architecture"
            ],
            "Marketing": [
                "Brand Strategy", "Customer Journey", "Omnichannel Experience",
                "Data-Driven Marketing", "Performance Marketing", "Conversion Optimization",
                "Customer Segmentation", "Personalization", "Engagement Strategy", "ROI-Focused"
            ],
            "Education": [
                "Pedagogical Excellence", "Learning Outcomes", "Curriculum Design",
                "Assessment Strategy", "Student-Centered", "Evidence-Based Teaching",
                "Differentiated Instruction", "Inclusive Education", "Digital Literacy"
            ]
        }
        
        # Enhanced platform-specific optimizations
        self.platform_specific = {
            "ChatGPT": [
                # Basic Prompting
                "Step by step", "Think step by step", "Let's work through this",
                "Break it down", "Provide examples", "Elaborate", "Clarify",
                "Explain like I'm five", "Chain of thought", "Advanced reasoning",
                
                # Advanced ChatGPT Techniques
                "Use the following format:", "First, let me understand...", "To solve this, I'll:",
                "Breaking this into components:", "Let me analyze each part:",
                "Consider multiple perspectives:", "Weighing the pros and cons:",
                "From first principles:", "Using analogies:", "Step-by-step methodology:",
                "Systematic approach:", "Structured analysis:", "Comprehensive evaluation:",
                "Take a deep breath and work on this problem step by step",
                "Think critically about:", "Apply logical reasoning:", "Use deductive logic:",
                "Consider edge cases:", "Validate assumptions:", "Cross-reference information:",
                
                # Output Control
                "Format as JSON:", "Create a table:", "Use bullet points:",
                "Provide numbered steps:", "Summarize key points:", "Include examples:",
                "Add implementation details:", "Specify requirements:", "Define success criteria:"
            ],
            
            "Claude": [
                # Core Claude Strengths
                "Comprehensive analysis", "Detailed explanation", "Thorough review",
                "In-depth", "Balanced perspective", "Comparative review",
                
                # Advanced Claude Techniques
                "Provide a nuanced analysis of:", "Consider multiple viewpoints on:",
                "Examine the ethical implications:", "Analyze the trade-offs between:",
                "Provide a scholarly perspective on:", "Offer a balanced assessment of:",
                "Draw connections between:", "Synthesize information from:",
                "Provide contextual background:", "Consider long-term implications:",
                "Evaluate critically:", "Assess objectively:", "Review systematically:",
                "Analyze comprehensively:", "Examine thoroughly:", "Investigate deeply:",
                
                # Claude's XML and Structure Support
                "Use <thinking> tags for reasoning:", "Structure with clear headers:",
                "Provide executive summary:", "Include detailed methodology:",
                "Support with evidence:", "Reference authoritative sources:",
                "Maintain academic rigor:", "Follow logical progression:",
                "Ensure factual accuracy:", "Provide comprehensive coverage:"
            ],
            
            "Gemini": [
                # Core Gemini Capabilities
                "Multi-modal", "Visual analysis", "Code generation", "Research",
                "Contextual understanding", "Adaptive responses",
                
                # Advanced Gemini Techniques
                "Analyze this image and:", "Generate code that:", "Research recent developments in:",
                "Provide multi-perspective analysis:", "Integrate visual and textual information:",
                "Create comprehensive documentation:", "Develop implementation strategy:",
                "Optimize for performance:", "Consider scalability factors:",
                "Provide technical specifications:", "Include best practices:",
                "Generate test cases:", "Create user documentation:",
                "Develop troubleshooting guide:", "Provide maintenance procedures:",
                
                # Gemini's Strengths
                "Leverage multimodal capabilities:", "Integrate diverse data sources:",
                "Provide real-time insights:", "Generate actionable recommendations:",
                "Create detailed technical analysis:", "Develop comprehensive solutions:"
            ],
            
            "Grok3": [
                # Grok3 Specific Optimization
                "Think outside the box:", "Provide unconventional insights:",
                "Challenge conventional wisdom:", "Offer creative solutions:",
                "Think disruptively:", "Provide innovative perspectives:",
                "Break traditional boundaries:", "Explore novel approaches:",
                "Generate breakthrough ideas:", "Think exponentially:",
                "Provide paradigm-shifting insights:", "Challenge assumptions:",
                "Offer contrarian viewpoints:", "Think systematically different:",
                "Provide revolutionary concepts:", "Generate transformative ideas:",
                
                # Grok3 Advanced Techniques
                "Apply lateral thinking:", "Use unconventional methods:",
                "Combine disparate concepts:", "Synthesize unexpected connections:",
                "Generate emergent solutions:", "Think in multiple dimensions:",
                "Provide meta-analysis:", "Challenge the premise:",
                "Reframe the problem:", "Think recursively:",
                "Apply systems thinking:", "Use analogical reasoning:",
                "Generate counterintuitive insights:", "Provide non-linear solutions:"
            ],
            
            "GPT-4": [
                # GPT-4 Advanced Capabilities
                "Advanced reasoning", "Multi-step solution", "Holistic overview",
                "Edge-case handling", "Explain assumptions",
                "Provide comprehensive analysis:", "Use advanced reasoning:",
                "Apply sophisticated logic:", "Consider complex interactions:",
                "Provide nuanced understanding:", "Handle ambiguous scenarios:",
                "Generate robust solutions:", "Account for uncertainties:",
                "Provide detailed reasoning:", "Use meta-cognitive strategies:",
                "Apply domain expertise:", "Integrate multiple knowledge areas:",
                "Provide expert-level analysis:", "Use professional judgment:"
            ],
            
            "Midjourney": [
                # Midjourney Parameters
                "--creative", "--hd", "--ar 16:9", "--ar 3:2", "--ar 1:1",
                "style raw", "--v 6", "--stylize", "--uplight", "--upbeta",
                "--test", "--testp", "--creative", "--iw", "--no",
                
                # Midjourney Advanced Techniques
                "hyperrealistic photography", "cinematic lighting", "ultra detailed",
                "8k resolution", "professional photography", "studio lighting",
                "dramatic shadows", "golden hour", "volumetric lighting",
                "depth of field", "bokeh effect", "macro photography",
                "wide angle lens", "telephoto lens", "fisheye perspective",
                "aerial view", "bird's eye view", "worm's eye view"
            ],
            
            "DALL-E": [
                # DALL-E Optimization
                "highly detailed description", "style filter", "higher resolution",
                "creative composition", "focused prompt", "artistic style",
                "professional quality", "studio lighting", "detailed textures",
                "realistic materials", "accurate proportions", "vivid colors",
                "dramatic contrast", "atmospheric perspective", "fine details",
                "photorealistic rendering", "artistic interpretation",
                "creative visualization", "imaginative concept"
            ],
            
            "Llama": [
                # Llama Optimization
                "Few-shot examples", "Prompt tuning", "Context window optimization",
                "Template-based prompting", "Instruction following",
                "Task-specific formatting", "Clear objective statement",
                "Explicit constraints", "Structured input format",
                "Expected output format", "Quality criteria specification"
            ],
            
            "Universal": [
                # Cross-Platform Techniques
                "Be specific and detailed:", "Provide clear instructions:",
                "Use concrete examples:", "Specify desired format:",
                "Include quality criteria:", "Define success metrics:",
                "Provide context and background:", "Specify constraints:",
                "Include relevant details:", "Request specific deliverables:",
                "Use professional language:", "Maintain consistent tone:",
                "Ensure clarity and precision:", "Provide comprehensive coverage:",
                "Include actionable recommendations:", "Specify implementation steps:"
            ]
        }
        
        # New category: Advanced Prompt Engineering Techniques
        self.prompt_techniques = [
            "Few-Shot Learning", "Zero-Shot Learning", "Chain-of-Thought",
            "Tree of Thoughts", "Self-Consistency", "Program-Aided Language Models",
            "Retrieval Augmented Generation", "In-Context Learning", "Prompt Chaining",
            "Constitutional AI", "Self-Refine", "Reflexion", "React Prompting",
            "Least-to-Most Prompting", "Generated Knowledge Prompting",
            "Automatic Prompt Engineering", "Gradient-Free Optimization",
            "Prompt Tuning", "P-Tuning", "Prefix Tuning", "LoRA Adaptation",
            "Instruction Tuning", "RLHF Training", "Constitutional Training",
            "Multi-Modal Prompting", "Cross-Modal Reasoning", "Modal Bridging"
        ]

    def get_suggestions(self, platform: str, category: str) -> List[str]:
        """Get enhancement suggestions based on platform and category"""
        suggestions = []
        
        # Add platform-specific suggestions
        if platform in self.platform_specific:
            suggestions.extend(self.platform_specific[platform][:8])
        elif platform != "Universal":
            suggestions.extend(self.platform_specific.get("Universal", [])[:5])
        
        # Add category-specific suggestions
        category_mappings = {
            "Creative": self.creative_terms,
            "Technical": self.technical_terms,
            "Business": self.quality_precision,
            "Academic": self.reasoning_frameworks,
            "General": self.style_modifiers
        }
        
        if category in category_mappings:
            suggestions.extend(category_mappings[category][:8])
        
        # Add general enhancements
        suggestions.extend(self.prompt_techniques[:5])
        suggestions.extend(self.output_formatting[:5])
        suggestions.extend(self.tone_voice[:5])
        
        return list(set(suggestions))  # Remove duplicates
    
    def get_industry_suggestions(self, industry: str) -> List[str]:
        """Get industry-specific enhancement suggestions"""
        return self.industry_terms.get(industry, [])
    
    def get_all_categories(self) -> Dict[str, List[str]]:
        """Return all enhancement categories"""
        return {
            "Style Modifiers": self.style_modifiers,
            "Technical Terms": self.technical_terms,
            "Creative Terms": self.creative_terms,
            "Reasoning Frameworks": self.reasoning_frameworks,
            "Output Formatting": self.output_formatting,
            "Tone & Voice": self.tone_voice,
            "Quality & Precision": self.quality_precision,
            "Prompt Techniques": self.prompt_techniques,
            "Platform Specific": self.platform_specific,
            "Industry Terms": self.industry_terms
        }
    
    def search_enhancements(self, query: str) -> List[str]:
        """Search for enhancements containing the query string"""
        results = []
        query_lower = query.lower()
        
        all_terms = (self.style_modifiers + self.technical_terms + 
                    self.creative_terms + self.reasoning_frameworks +
                    self.output_formatting + self.tone_voice + 
                    self.quality_precision + self.prompt_techniques)
        
        # Add platform-specific terms
        for platform_terms in self.platform_specific.values():
            all_terms.extend(platform_terms)
        
        # Add industry terms
        for industry_terms in self.industry_terms.values():
            all_terms.extend(industry_terms)
        
        for term in all_terms:
            if query_lower in term.lower():
                results.append(term)
        
        return list(set(results))  # Remove duplicates
    
    def get_random_enhancement(self, count: int = 5) -> List[str]:
        """Get random enhancement suggestions"""
        all_terms = (self.style_modifiers + self.technical_terms + 
                    self.creative_terms + self.reasoning_frameworks +
                    self.output_formatting + self.tone_voice + 
                    self.quality_precision + self.prompt_techniques)
        
        return random.sample(all_terms, min(count, len(all_terms)))
    
    def get_enhancement_by_type(self, enhancement_type: str, count: int = 10) -> List[str]:
        """Get specific type of enhancements"""
        type_mapping = {
            "style": self.style_modifiers,
            "technical": self.technical_terms,
            "creative": self.creative_terms,
            "reasoning": self.reasoning_frameworks,
            "formatting": self.output_formatting,
            "tone": self.tone_voice,
            "quality": self.quality_precision,
            "techniques": self.prompt_techniques
        }
        
        enhancement_list = type_mapping.get(enhancement_type.lower(), [])
        return enhancement_list[:count]


class PromptStorage:
    def __init__(self, file_path: str = "prompts.json"):
        self.file_path = Path(file_path)
        self.backup_path = Path(f"{file_path}.backup")
        self.prompts: Dict[str, Prompt] = {}
        self.load_prompts()
    
    def load_prompts(self) -> None:
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for prompt_data in data.get('prompts', []):
                        prompt = Prompt(**prompt_data)
                        self.prompts[prompt.id] = prompt
        except Exception as e:
            if self.backup_path.exists():
                self.restore_from_backup()
    
    def save_prompts(self) -> bool:
        try:
            if self.file_path.exists():
                self.file_path.replace(self.backup_path)
            
            data = {
                'version': '1.0',
                'created_at': datetime.now().isoformat(),
                'prompts': [asdict(prompt) for prompt in self.prompts.values()]
            }
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def restore_from_backup(self) -> None:
        if self.backup_path.exists():
            self.backup_path.replace(self.file_path)
            self.load_prompts()
    
    def add_prompt(self, prompt: Prompt) -> bool:
        self.prompts[prompt.id] = prompt
        return self.save_prompts()
    
    def update_prompt(self, prompt: Prompt) -> bool:
        if prompt.id in self.prompts:
            prompt.modified_at = datetime.now().isoformat()
            self.prompts[prompt.id] = prompt
            return self.save_prompts()
        return False
    
    def delete_prompt(self, prompt_id: str) -> bool:
        if prompt_id in self.prompts:
            del self.prompts[prompt_id]
            return self.save_prompts()
        return False
    
    def get_prompts(self, platform: str = None, category: str = None) -> List[Prompt]:
        prompts = list(self.prompts.values())
        if platform:
            prompts = [p for p in prompts if p.platform == platform]
        if category:
            prompts = [p for p in prompts if p.category == category]
        return sorted(prompts, key=lambda x: x.modified_at, reverse=True)
    
    def search_prompts(self, query: str) -> List[Prompt]:
        query_lower = query.lower()
        return [
            prompt for prompt in self.prompts.values()
            if query_lower in prompt.title.lower() or 
               query_lower in prompt.content.lower() or
               any(query_lower in tag.lower() for tag in prompt.tags)
        ]


class PromptEditor(QWidget):
    prompt_saved = pyqtSignal(Prompt)
    
    def __init__(self, enhancement_lib: EnhancementLibrary):
        super().__init__()
        self.enhancement_lib = enhancement_lib
        self.current_prompt: Optional[Prompt] = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create tab widget for enhanced interface
        self.tab_widget = QTabWidget()
        
        # Basic Info Tab
        basic_tab = QWidget()
        basic_layout = QVBoxLayout(basic_tab)
        
        form_layout = QFormLayout()
        self.title_edit = QLineEdit()
        self.platform_combo = QComboBox()
        self.platform_combo.addItems([
            "Universal", "ChatGPT", "Claude", "Gemini", "Grok3", 
            "GPT-4", "Midjourney", "DALL-E", "Llama"
        ])
        self.category_edit = QLineEdit()
        
        form_layout.addRow("Title:", self.title_edit)
        form_layout.addRow("Platform:", self.platform_combo)
        form_layout.addRow("Category:", self.category_edit)
        
        basic_layout.addLayout(form_layout)
        
        # Content editor
        self.content_edit = QTextEdit()
        self.content_edit.setMinimumHeight(300)
        self.content_edit.setFont(QFont("Consolas", 11))
        basic_layout.addWidget(QLabel("Prompt Content:"))
        basic_layout.addWidget(self.content_edit)
        
        # Tags section
        tags_layout = QHBoxLayout()
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Enter tags separated by commas...")
        tags_layout.addWidget(QLabel("Tags:"))
        tags_layout.addWidget(self.tags_edit)
        basic_layout.addLayout(tags_layout)
        
        self.tab_widget.addTab(basic_tab, "Basic Info")
        
        # Enhancement Tools Tab
        enhancement_tab = QWidget()
        enhancement_layout = QVBoxLayout(enhancement_tab)
        
        # Enhancement category selector
        category_layout = QHBoxLayout()
        self.enhancement_category = QComboBox()
        self.enhancement_category.addItems([
            "All Suggestions", "Style Modifiers", "Technical Terms", "Creative Terms",
            "Reasoning Frameworks", "Output Formatting", "Tone & Voice",
            "Quality & Precision", "Prompt Techniques", "Platform Specific"
        ])
        self.enhancement_category.currentTextChanged.connect(self.update_enhancements)
        
        self.industry_combo = QComboBox()
        self.industry_combo.addItems([
            "General", "Healthcare", "Finance", "Technology", "Marketing", "Education", "Programming"
        ])
        self.industry_combo.currentTextChanged.connect(self.update_enhancements)
        
        category_layout.addWidget(QLabel("Category:"))
        category_layout.addWidget(self.enhancement_category)
        category_layout.addWidget(QLabel("Industry:"))
        category_layout.addWidget(self.industry_combo)
        enhancement_layout.addLayout(category_layout)
        
        # Enhancement selection
        self.enhancement_combo = QComboBox()
        self.enhancement_combo.currentTextChanged.connect(self.insert_enhancement)
        enhancement_layout.addWidget(QLabel("Select Enhancement:"))
        enhancement_layout.addWidget(self.enhancement_combo)
        
        # Enhancement search
        search_layout = QHBoxLayout()
        self.enhancement_search = QLineEdit()
        self.enhancement_search.setPlaceholderText("Search enhancements...")
        self.enhancement_search.textChanged.connect(self.search_enhancements)
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_enhancements)
        
        search_layout.addWidget(self.enhancement_search)
        search_layout.addWidget(search_button)
        enhancement_layout.addLayout(search_layout)
        
        # Quick enhancement buttons
        quick_buttons_layout = QVBoxLayout()
        quick_buttons_layout.addWidget(QLabel("Quick Enhancements:"))
        
        button_row1 = QHBoxLayout()
        self.style_button = QPushButton("Add Style")
        self.technical_button = QPushButton("Add Technical")
        self.creative_button = QPushButton("Add Creative")
        
        button_row1.addWidget(self.style_button)
        button_row1.addWidget(self.technical_button)
        button_row1.addWidget(self.creative_button)
        quick_buttons_layout.addLayout(button_row1)
        
        button_row2 = QHBoxLayout()
        self.reasoning_button = QPushButton("Add Reasoning")
        self.format_button = QPushButton("Add Formatting")
        self.random_button = QPushButton("Random Mix")
        
        button_row2.addWidget(self.reasoning_button)
        button_row2.addWidget(self.format_button)
        button_row2.addWidget(self.random_button)
        quick_buttons_layout.addLayout(button_row2)
        
        enhancement_layout.addLayout(quick_buttons_layout)
        
        # Enhancement preview area
        self.enhancement_preview = QTextEdit()
        self.enhancement_preview.setMaximumHeight(100)
        self.enhancement_preview.setPlaceholderText("Enhancement suggestions will appear here...")
        enhancement_layout.addWidget(QLabel("Enhancement Preview:"))
        enhancement_layout.addWidget(self.enhancement_preview)
        
        self.tab_widget.addTab(enhancement_tab, "Enhancements")
        
        # Advanced Options Tab
        advanced_tab = QWidget()
        advanced_layout = QVBoxLayout(advanced_tab)
        
        # Quality settings
        quality_group = QGroupBox("Quality Settings")
        quality_layout = QFormLayout(quality_group)
        
        self.precision_slider = QSpinBox()
        self.precision_slider.setRange(1, 10)
        self.precision_slider.setValue(5)
        
        self.creativity_slider = QSpinBox()
        self.creativity_slider.setRange(1, 10)
        self.creativity_slider.setValue(5)
        
        quality_layout.addRow("Precision Level:", self.precision_slider)
        quality_layout.addRow("Creativity Level:", self.creativity_slider)
        
        advanced_layout.addWidget(quality_group)
        
        # Auto-enhancement options
        auto_group = QGroupBox("Auto-Enhancement")
        auto_layout = QVBoxLayout(auto_group)
        
        self.auto_platform_checkbox = QCheckBox("Auto-add platform optimizations")
        self.auto_quality_checkbox = QCheckBox("Auto-add quality modifiers")
        self.auto_structure_checkbox = QCheckBox("Auto-add structure guidance")
        
        auto_layout.addWidget(self.auto_platform_checkbox)
        auto_layout.addWidget(self.auto_quality_checkbox)
        auto_layout.addWidget(self.auto_structure_checkbox)
        
        advanced_layout.addWidget(auto_group)
        advanced_layout.addStretch()
        
        self.tab_widget.addTab(advanced_tab, "Advanced")
        
        layout.addWidget(self.tab_widget)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Prompt")
        self.clear_button = QPushButton("Clear")
        self.optimize_button = QPushButton("Auto-Optimize")
        
        self.save_button.clicked.connect(self.save_prompt)
        self.clear_button.clicked.connect(self.clear_form)
        self.optimize_button.clicked.connect(self.auto_optimize)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.optimize_button)
        layout.addLayout(button_layout)
        
        # Connect signals for quick buttons
        self.style_button.clicked.connect(lambda: self.insert_quick_enhancement("style"))
        self.technical_button.clicked.connect(lambda: self.insert_quick_enhancement("technical"))
        self.creative_button.clicked.connect(lambda: self.insert_quick_enhancement("creative"))
        self.reasoning_button.clicked.connect(lambda: self.insert_quick_enhancement("reasoning"))
        self.format_button.clicked.connect(lambda: self.insert_quick_enhancement("formatting"))
        self.random_button.clicked.connect(lambda: self.insert_quick_enhancement("random"))
        
        self.platform_combo.currentTextChanged.connect(self.update_enhancements)
        self.update_enhancements()
    
    def update_enhancements(self):
        platform = self.platform_combo.currentText()
        category = self.enhancement_category.currentText()
        industry = self.industry_combo.currentText()
        
        suggestions = []
        
        if category == "All Suggestions":
            suggestions = self.enhancement_lib.get_suggestions(platform, "")
        elif category == "Platform Specific":
            suggestions = self.enhancement_lib.platform_specific.get(platform, [])
        else:
            category_map = {
                "Style Modifiers": "style",
                "Technical Terms": "technical", 
                "Creative Terms": "creative",
                "Reasoning Frameworks": "reasoning",
                "Output Formatting": "formatting",
                "Tone & Voice": "tone",
                "Quality & Precision": "quality",
                "Prompt Techniques": "techniques"
            }
            if category in category_map:
                suggestions = self.enhancement_lib.get_enhancement_by_type(category_map[category], 20)
        
        # Add industry-specific suggestions
        if industry != "General":
            industry_suggestions = self.enhancement_lib.get_industry_suggestions(industry)
            suggestions.extend(industry_suggestions)
        
        self.enhancement_combo.clear()
        self.enhancement_combo.addItem("Select enhancement...")
        self.enhancement_combo.addItems(suggestions[:50])  # Limit for performance
    
    def search_enhancements(self):
        query = self.enhancement_search.text().strip()
        if query:
            results = self.enhancement_lib.search_enhancements(query)
            self.enhancement_combo.clear()
            self.enhancement_combo.addItem("Search results...")
            self.enhancement_combo.addItems(results[:30])
    
    def insert_enhancement(self, text: str):
        if text not in ["Select enhancement...", "Search results..."]:
            cursor = self.content_edit.textCursor()
            cursor.insertText(f"{text} ")
            self.enhancement_combo.setCurrentIndex(0)
            
            # Update preview
            self.enhancement_preview.append(f"Added: {text}")
    
    def insert_quick_enhancement(self, enhancement_type: str):
        if enhancement_type == "random":
            enhancements = self.enhancement_lib.get_random_enhancement(3)
        else:
            enhancements = self.enhancement_lib.get_enhancement_by_type(enhancement_type, 3)
        
        cursor = self.content_edit.textCursor()
        for enhancement in enhancements:
            cursor.insertText(f"{enhancement} ")
        
        # Update preview
        self.enhancement_preview.append(f"Added {enhancement_type}: {', '.join(enhancements)}")
    
    def auto_optimize(self):
        """Auto-optimize the prompt based on current settings"""
        platform = self.platform_combo.currentText()
        content = self.content_edit.toPlainText()
        
        optimizations = []
        
        if self.auto_platform_checkbox.isChecked():
            platform_opts = self.enhancement_lib.platform_specific.get(platform, [])
            if platform_opts:
                optimizations.extend(platform_opts[:2])
        
        if self.auto_quality_checkbox.isChecked():
            quality_opts = self.enhancement_lib.get_enhancement_by_type("quality", 2)
            optimizations.extend(quality_opts)
        
        if self.auto_structure_checkbox.isChecked():
            structure_opts = self.enhancement_lib.get_enhancement_by_type("formatting", 2)
            optimizations.extend(structure_opts)
        
        if optimizations:
            optimized_content = content + "\n\nOptimizations: " + " ".join(optimizations)
            self.content_edit.setPlainText(optimized_content)
            
            self.enhancement_preview.append(f"Auto-optimized with: {', '.join(optimizations)}")
    
    def load_prompt(self, prompt: Prompt):
        self.current_prompt = prompt
        self.title_edit.setText(prompt.title)
        self.platform_combo.setCurrentText(prompt.platform)
        self.category_edit.setText(prompt.category)
        self.content_edit.setPlainText(prompt.content)
        self.tags_edit.setText(", ".join(prompt.tags))
    
    def clear_form(self):
        self.current_prompt = None
        self.title_edit.clear()
        self.platform_combo.setCurrentIndex(0)
        self.category_edit.clear()
        self.content_edit.clear()
        self.tags_edit.clear()
        self.enhancement_preview.clear()
        self.enhancement_search.clear()
    
    def save_prompt(self):
        if not self.title_edit.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter a title for the prompt.")
            return
        
        if not self.content_edit.toPlainText().strip():
            QMessageBox.warning(self, "Warning", "Please enter content for the prompt.")
            return
        
        # Parse tags
        tags = [tag.strip() for tag in self.tags_edit.text().split(",") if tag.strip()]
        
        if self.current_prompt:
            prompt = self.current_prompt
            prompt.title = self.title_edit.text().strip()
            prompt.platform = self.platform_combo.currentText()
            prompt.category = self.category_edit.text().strip()
            prompt.content = self.content_edit.toPlainText().strip()
            prompt.tags = tags
            prompt.modified_at = datetime.now().isoformat()
        else:
            prompt = Prompt(
                id=str(uuid.uuid4()),
                title=self.title_edit.text().strip(),
                content=self.content_edit.toPlainText().strip(),
                platform=self.platform_combo.currentText(),
                category=self.category_edit.text().strip(),
                created_at=datetime.now().isoformat(),
                modified_at=datetime.now().isoformat(),
                tags=tags
            )
        
        self.prompt_saved.emit(prompt)
        QMessageBox.information(self, "Success", "Prompt saved successfully!")


class PromptList(QListWidget):
    prompt_selected = pyqtSignal(Prompt)
    prompt_deleted = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.prompts: Dict[str, Prompt] = {}
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
    
    def add_prompt(self, prompt: Prompt):
        self.prompts[prompt.id] = prompt
        item = QListWidgetItem(f"{prompt.title} [{prompt.platform}]")
        item.setData(Qt.ItemDataRole.UserRole, prompt.id)
        self.addItem(item)
    
    def update_prompts(self, prompts: List[Prompt]):
        self.clear()
        self.prompts.clear()
        for prompt in prompts:
            self.add_prompt(prompt)
    
    def on_item_double_clicked(self, item: QListWidgetItem):
        prompt_id = item.data(Qt.ItemDataRole.UserRole)
        if prompt_id in self.prompts:
            self.prompt_selected.emit(self.prompts[prompt_id])
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            current_item = self.currentItem()
            if current_item:
                prompt_id = current_item.data(Qt.ItemDataRole.UserRole)
                reply = QMessageBox.question(
                    self, "Delete Prompt", 
                    "Are you sure you want to delete this prompt?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.prompt_deleted.emit(prompt_id)
                    self.takeItem(self.row(current_item))
                    del self.prompts[prompt_id]
        super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.storage = PromptStorage()
        self.enhancement_lib = EnhancementLibrary()
        self.setup_ui()
        self.setup_menu()
        self.load_prompts()
    
    def setup_ui(self):
        self.setWindowTitle("Prompt Management System")
        self.setGeometry(100, 100, 1400, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        
        left_panel = QWidget()
        left_panel.setMaximumWidth(450)
        left_layout = QVBoxLayout(left_panel)
        
        # Enhanced search and filter section
        search_group = QGroupBox("Search & Filter")
        search_layout = QVBoxLayout(search_group)
        
        # Search box
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search prompts...")
        self.search_edit.textChanged.connect(self.search_prompts)
        search_layout.addWidget(self.search_edit)
        
        # Filter options
        filter_layout = QHBoxLayout()
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "All", "Universal", "ChatGPT", "Claude", "Gemini", "Grok3",
            "GPT-4", "Midjourney", "DALL-E", "Llama"
        ])
        self.filter_combo.currentTextChanged.connect(self.filter_prompts)
        
        self.category_filter = QComboBox()
        self.category_filter.addItems([
            "All Categories", "Creative", "Technical", "Business", "Academic", "General"
        ])
        self.category_filter.currentTextChanged.connect(self.filter_by_category)
        
        filter_layout.addWidget(QLabel("Platform:"))
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(QLabel("Category:"))
        filter_layout.addWidget(self.category_filter)
        search_layout.addLayout(filter_layout)
        
        left_layout.addWidget(search_group)
        
        # Prompt list
        self.prompt_list = PromptList()
        self.prompt_list.prompt_selected.connect(self.load_prompt_for_editing)
        self.prompt_list.prompt_deleted.connect(self.delete_prompt)
        left_layout.addWidget(self.prompt_list)
        
        # Action buttons
        button_layout = QHBoxLayout()
        new_prompt_button = QPushButton("New Prompt")
        new_prompt_button.clicked.connect(self.new_prompt)
        
        template_button = QPushButton("From Template")
        template_button.clicked.connect(self.create_from_template)
        
        button_layout.addWidget(new_prompt_button)
        button_layout.addWidget(template_button)
        left_layout.addLayout(button_layout)
        
        # Enhanced editor
        self.editor = PromptEditor(self.enhancement_lib)
        self.editor.prompt_saved.connect(self.save_prompt)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.editor)
        splitter.setSizes([450, 950])
        
        layout.addWidget(splitter)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status()
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Prompt", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_prompt)
        file_menu.addAction(new_action)
        
        export_action = QAction("Export Prompts", self)
        export_action.triggered.connect(self.export_prompts)
        file_menu.addAction(export_action)
        
        import_action = QAction("Import Prompts", self)
        import_action.triggered.connect(self.import_prompts)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction("Create Backup", self)
        backup_action.triggered.connect(self.create_backup)
        file_menu.addAction(backup_action)
        
        restore_action = QAction("Restore Backup", self)
        restore_action.triggered.connect(self.restore_backup)
        file_menu.addAction(restore_action)
        
        # Tools Menu
        tools_menu = menubar.addMenu("Tools")
        
        enhancement_browser = QAction("Enhancement Browser", self)
        enhancement_browser.triggered.connect(self.show_enhancement_browser)
        tools_menu.addAction(enhancement_browser)
        
        bulk_optimize = QAction("Bulk Optimize", self)
        bulk_optimize.triggered.connect(self.bulk_optimize_prompts)
        tools_menu.addAction(bulk_optimize)
        
        # Help Menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_from_template(self):
        """Create a new prompt from template"""
        templates = {
            "Creative Writing": "Create a compelling [TYPE] that [OBJECTIVE]. Use [STYLE] tone and include [ELEMENTS]. The target audience is [AUDIENCE].",
            "Technical Analysis": "Analyze [SUBJECT] using [METHODOLOGY]. Provide step-by-step breakdown, identify key components, and deliver actionable recommendations.",
            "Business Strategy": "Develop a comprehensive strategy for [BUSINESS_GOAL]. Consider market conditions, competitive landscape, and resource constraints.",
            "Code Review": "Review the following code for [LANGUAGE]. Check for best practices, performance optimization, security vulnerabilities, and maintainability.",
            "Data Analysis": "Analyze the provided data to identify patterns, trends, and insights. Use statistical methods and provide visual representations where appropriate.",
            "Bug Report": "Document a bug found in [SYSTEM]. Include steps to reproduce, expected behavior, actual behavior, and environment details.",
            "API Design": "Design an API for [USE_CASE]. Specify endpoints, request/response formats, authentication method, and error handling.",
            "Database Schema": "Create a database schema to support [APPLICATION]. Include tables, relationships, and indexing strategies.",
            "Script Generator": "Generate a script in [LANGUAGE] to automate [TASK]. Include comments, input validation, and error handling.",
            "Security Audit": "Perform a security audit on [SYSTEM/PROJECT]. Highlight vulnerabilities, recommend fixes, and assess risk level.",
            "Pitch Deck": "Build a pitch deck for [STARTUP/PRODUCT] targeting [INVESTOR TYPE]. Include problem, solution, market size, traction, and business model.",
            "Marketing Copy": "Write persuasive marketing copy for [PRODUCT]. Highlight unique selling points, benefits, and a clear call-to-action.",
            "Brand Voice Guide": "Define a brand voice for [COMPANY]. Include tone, vocabulary, dos/don'ts, and example statements.",
            "Campaign Strategy": "Develop a marketing campaign for [GOAL]. Define channels, timeline, KPIs, and creative direction.",
            "User Persona": "Create a detailed persona for [PRODUCT]. Include demographics, behavior patterns, goals, and pain points.",
            "Lesson Plan": "Design a lesson plan for [TOPIC] targeting [GRADE_LEVEL]. Include objectives, materials, and activity steps.",
            "Quiz Generator": "Create a [FORMAT] quiz on [SUBJECT]. Include questions, answer options, and explanations for each correct answer.",
            "Study Guide": "Develop a study guide for [TOPIC]. Cover key concepts, summaries, definitions, and practice exercises.",
            "Concept Explanation": "Explain [TOPIC] in simple terms for [AUDIENCE]. Use analogies, visuals, and examples to aid understanding.",
            "Curriculum Outline": "Create a curriculum for [SUBJECT] over [TIME_PERIOD]. Divide into modules with clear learning objectives.",
            "Prompt Builder": "Design a reusable prompt for [MODEL_TYPE] to perform [TASK]. Ensure clarity, specificity, and modularity.",
            "Chain-of-Thought Prompt": "Create a CoT prompt that walks through [PROBLEM TYPE]. Encourage stepwise reasoning and error checks.",
            "System Message Template": "Write a system prompt for an AI assistant specializing in [DOMAIN]. Define tone, rules, and limits.",
            "Few-Shot Prompt": "Build a few-shot learning prompt for [TASK]. Include diverse examples, clear input/output separation, and task framing.",
            "Critique Prompt": "Generate a prompt that makes the model critique [CONTENT_TYPE] for quality, clarity, and relevance.",
            "Meeting Agenda": "Create an agenda for a meeting on [TOPIC]. Include objectives, discussion points, and time allocations.",
            "Workflow Optimization": "Design an optimized workflow for [PROCESS]. Identify bottlenecks, propose automation, and assign roles.",
            "Email Template": "Write a professional email for [SCENARIO]. Maintain clarity, proper tone, and include key points.",
            "Checklist": "Build a checklist for [ACTIVITY]. Ensure all critical steps are listed and sequenced logically.",
            "SOP Document": "Write a Standard Operating Procedure for [TASK]. Include purpose, scope, responsibilities, and step-by-step actions.",
            "Research Summary": "Summarize findings from [STUDY_TYPE] on [TOPIC]. Highlight objectives, methods, results, and implications.",
            "Lab Report": "Write a lab report for [EXPERIMENT]. Include hypothesis, setup, observations, data analysis, and conclusion.",
            "Technical Specification": "Draft a technical spec for [PRODUCT/SYSTEM]. Cover features, design constraints, materials, and standards.",
            "Patent Abstract": "Write a concise patent abstract for [INVENTION]. Clearly state novelty, functionality, and potential applications.",
            "Scientific Proposal": "Develop a proposal for a study on [TOPIC]. Include background, research question, methodology, and expected impact."
        }
        
        template_name, ok = QMessageBox.question(
            self, "Select Template", 
            "Choose a template:\n" + "\n".join(templates.keys()),
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        
        if ok:
            # For simplicity, using the first template
            self.editor.clear_form()
            self.editor.content_edit.setPlainText(list(templates.values())[0])
    
    def show_enhancement_browser(self):
        """Show enhancement browser dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Enhancement Browser")
        dialog.setGeometry(200, 200, 800, 600)
        
        layout = QVBoxLayout(dialog)
        
        # Category tree
        tree = QTreeWidget()
        tree.setHeaderLabels(["Category", "Count"])
        
        categories = self.enhancement_lib.get_all_categories()
        for category, items in categories.items():
            if isinstance(items, dict):  # Handle nested dictionaries
                parent = QTreeWidgetItem([category, str(len(items))])
                for subcategory, subitems in items.items():
                    child = QTreeWidgetItem([subcategory, str(len(subitems))])
                    parent.addChild(child)
            else:
                parent = QTreeWidgetItem([category, str(len(items))])
            tree.addTopLevelItem(parent)
        
        layout.addWidget(tree)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        
        dialog.exec()
    
    def bulk_optimize_prompts(self):
        """Bulk optimize all prompts"""
        reply = QMessageBox.question(
            self, "Bulk Optimize", 
            "This will add platform-specific optimizations to all prompts. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            optimized_count = 0
            for prompt in self.storage.prompts.values():
                platform_opts = self.enhancement_lib.platform_specific.get(prompt.platform, [])
                if platform_opts and not any(opt in prompt.content for opt in platform_opts[:3]):
                    prompt.content += f"\n\nOptimizations: {' '.join(platform_opts[:3])}"
                    self.storage.update_prompt(prompt)
                    optimized_count += 1
            
            self.load_prompts()
            QMessageBox.information(self, "Success", f"Optimized {optimized_count} prompts!")
    
    def filter_by_category(self, category: str):
        """Filter prompts by category"""
        if category == "All Categories":
            prompts = self.storage.get_prompts()
        else:
            prompts = self.storage.get_prompts(category=category)
        self.prompt_list.update_prompts(prompts)
    
    def load_prompts(self):
        prompts = self.storage.get_prompts()
        self.prompt_list.update_prompts(prompts)
        self.update_status()
    
    def save_prompt(self, prompt: Prompt):
        if prompt.id in self.storage.prompts:
            success = self.storage.update_prompt(prompt)
        else:
            success = self.storage.add_prompt(prompt)
        
        if success:
            self.load_prompts()
            self.editor.clear_form()
        else:
            QMessageBox.critical(self, "Error", "Failed to save prompt.")
    
    def delete_prompt(self, prompt_id: str):
        success = self.storage.delete_prompt(prompt_id)
        if success:
            self.update_status()
        else:
            QMessageBox.critical(self, "Error", "Failed to delete prompt.")
    
    def load_prompt_for_editing(self, prompt: Prompt):
        self.editor.load_prompt(prompt)
    
    def new_prompt(self):
        self.editor.clear_form()
    
    def search_prompts(self, query: str):
        if query.strip():
            prompts = self.storage.search_prompts(query)
        else:
            prompts = self.storage.get_prompts()
        self.prompt_list.update_prompts(prompts)
    
    def filter_prompts(self, platform: str):
        if platform == "All":
            prompts = self.storage.get_prompts()
        else:
            prompts = self.storage.get_prompts(platform=platform)
        self.prompt_list.update_prompts(prompts)
    
    def export_prompts(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Prompts", "prompts_export.json", "JSON Files (*.json)"
        )
        if file_path:
            try:
                data = {
                    'exported_at': datetime.now().isoformat(),
                    'prompts': [asdict(prompt) for prompt in self.storage.prompts.values()]
                }
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "Success", "Prompts exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export prompts: {str(e)}")
    
    def import_prompts(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Prompts", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                imported_count = 0
                for prompt_data in data.get('prompts', []):
                    prompt = Prompt(**prompt_data)
                    if prompt.id not in self.storage.prompts:
                        self.storage.add_prompt(prompt)
                        imported_count += 1
                
                self.load_prompts()
                QMessageBox.information(
                    self, "Success", f"Imported {imported_count} new prompts!"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import prompts: {str(e)}")
    
    def create_backup(self):
        success = self.storage.save_prompts()
        if success:
            QMessageBox.information(self, "Success", "Backup created successfully!")
        else:
            QMessageBox.critical(self, "Error", "Failed to create backup.")
    
    def restore_backup(self):
        reply = QMessageBox.question(
            self, "Restore Backup", 
            "This will replace current prompts with the backup. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.storage.restore_from_backup()
            self.load_prompts()
            QMessageBox.information(self, "Success", "Backup restored successfully!")
    
    def show_about(self):
        QMessageBox.about(self, "About", 
                         "Prompt Engineer V1.0 Made By xeQter 2025.\n\n"
                         "Professional prompt engineering toolkit with advanced "
                         "enhancement capabilities for:\nChatGPT, Claude, Gemini, "
                         "Grok3, and other AI platforms.\n\n"
                         "Features: \nWORK IN PROGRESS! MORE WILL COME SOON")
    
    def update_status(self):
        total_prompts = len(self.storage.prompts)
        enhancement_count = len(self.enhancement_lib.style_modifiers + 
                                self.enhancement_lib.technical_terms + 
                                self.enhancement_lib.creative_terms)
        self.status_bar.showMessage(
            f"Total Prompts: {total_prompts} | Enhancement Library: {enhancement_count}+ terms"
        )


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application properties
    app.setApplicationName("Prompt Engineer - Made By xeQted")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Prompt Engineering Solutions")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
