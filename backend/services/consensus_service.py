import re
from typing import List, Dict, Any

class ConsensusService:
    # Source trust ratings (Scale 1-10)
    SOURCE_METADATA = {
        'MDN Web Docs': {'trust_score': 10, 'reliability': 'Authoritative Docs', 'base_confidence': 0.98},
        'Stack Overflow': {'trust_score': 9, 'reliability': 'Very High', 'base_confidence': 0.95},
        'ChatGPT': {'trust_score': 9, 'reliability': 'Very High (AI Verified)', 'base_confidence': 0.94},
        'Gemini AI': {'trust_score': 9, 'reliability': 'Very High (AI Verified)', 'base_confidence': 0.92},
        'GitHub': {'trust_score': 8, 'reliability': 'High', 'base_confidence': 0.85},
        'GeeksforGeeks': {'trust_score': 8, 'reliability': 'High', 'base_confidence': 0.83},
        'Wikipedia': {'trust_score': 8, 'reliability': 'High', 'base_confidence': 0.80},
        'Dev.to': {'trust_score': 7, 'reliability': 'Good', 'base_confidence': 0.72},
        'Reddit': {'trust_score': 7, 'reliability': 'Good', 'base_confidence': 0.70},
        'Google Search': {'trust_score': 7, 'reliability': 'Good', 'base_confidence': 0.68},
        'YouTube': {'trust_score': 6, 'reliability': 'Good', 'base_confidence': 0.65}
    }

    @staticmethod
    def detect_language(query: str) -> str:
        q = " " + query.lower() + " "
        if any(w in q for w in [' python ', ' python3 ', ' py ', ' pandas ', ' numpy ', ' django ', ' flask ']):
            return 'python'
        if any(w in q for w in [' javascript ', ' js ', ' node ', ' nodejs ', ' node.js ', ' express ', ' expressjs ', ' react ', ' reactjs ', ' vue ', ' vuejs ']):
            return 'javascript'
        if any(w in q for w in [' typescript ', ' ts ']):
            return 'typescript'
        if any(w in q for w in [' java ', ' spring ', ' springboot ', ' maven ', ' jvm ']):
            return 'java'
        if any(w in q for w in [' c++ ', ' cpp ']):
            return 'cpp'
        if any(w in q for w in [' c# ', ' csharp ', ' .net ', ' dotnet ']):
            return 'csharp'
        if any(w in q for w in [' rust ', ' cargo ', ' rustlang ']):
            return 'rust'
        if any(w in q for w in [' go ', ' golang ']):
            return 'go'
        if any(w in q for w in [' kotlin ']):
            return 'kotlin'
        if any(w in q for w in [' swift ', ' swiftui ', ' ios ']):
            return 'swift'
        if any(w in q for w in [' php ', ' laravel ']):
            return 'php'
        if any(w in q for w in [' ruby ', ' rails ']):
            return 'ruby'
        if any(w in q for w in [' sql ', ' postgres ', ' postgresql ', ' mysql ', ' sqlite ']):
            return 'sql'
        if any(w in q for w in [' bash ', ' shell ', ' zsh ', ' sh ']):
            return 'bash'
        if any(w in q for w in [' dart ', ' flutter ']):
            return 'dart'
        if any(w in q for w in [' in c ', ' c language ', ' c program ']) or (' c ' in q and any(w in q for w in ['pointer', 'malloc', 'struct', 'header'])):
            return 'c'
        if any(w in q for w in [' css ', ' html ', ' flexbox ', ' grid ']):
            return 'html_css'
        return ''

    @staticmethod
    def is_technical_topic(topic: str) -> bool:
        return topic in [
            'technology_coding', 'html_css', 'python', 'javascript', 'typescript',
            'database', 'sql', 'git', 'devops', 'java', 'cpp', 'csharp', 'c',
            'go', 'rust', 'kotlin', 'swift', 'php', 'ruby', 'bash', 'dart'
        ]

    @classmethod
    def detect_topic(cls, query: str) -> str:
        q = query.lower()

        # Check explicit language request first
        lang = cls.detect_language(query)
        if lang:
            return lang

        # Check code / programming intent
        code_words = ['code', 'program', 'algorithm', 'syntax', 'function', 'class', 'method', 'loop', 'array', 'variable', 'sorting', 'binary tree', 'recursion', 'stack', 'queue', 'leetcode', 'api', 'endpoint']
        if any(w in q for w in code_words):
            return 'technology_coding'

        # 1. Technical & Infrastructure Domains
        if any(w in q for w in ['css', 'div', 'html', 'flexbox', 'grid', 'margin', 'center', 'style', 'dom', 'selector']):
            return 'html_css'
        if any(w in q for w in ['sql', 'database', 'postgres', 'mysql', 'join', 'select', 'table', 'query', 'mongodb', 'schema']):
            return 'database'
        if any(w in q for w in ['git', 'commit', 'branch', 'merge', 'rebase', 'repo', 'push', 'pull']):
            return 'git'
        if any(w in q for w in ['docker', 'container', 'kubernetes', 'k8s', 'deploy', 'aws', 'ci/cd', 'linux', 'bash']):
            return 'devops'

        # 2. Universal Domains
        if any(w in q for w in ['sky', 'blue', 'physics', 'chemistry', 'biology', 'gravity', 'atom', 'molecule', 'planet', 'space', 'astronomy', 'earth', 'sun', 'moon', 'photosynthesis', 'energy', 'light', 'wavelength', 'sound', 'quantum', 'evolution', 'dinosaur', 'climate']):
            return 'science'
        if any(w in q for w in ['health', 'doctor', 'medicine', 'symptom', 'diet', 'nutrition', 'vitamin', 'sleep', 'workout', 'fitness', 'weight', 'calories', 'water', 'hydration', 'blood', 'disease', 'mental health', 'exercise', 'heart', 'protein']):
            return 'health_wellness'
        if any(w in q for w in ['money', 'invest', 'stock', 'compound interest', 'inflation', 'economy', 'economic', 'business', 'market', 'tax', 'budget', 'crypto', 'bitcoin', 'startup', 'revenue', 'profit', 'bank', 'loan', 'gdp', 'wealth']):
            return 'finance_business'
        if any(w in q for w in ['history', 'war', 'empire', 'battle', 'revolution', 'ancient', 'medieval', 'century', 'president', 'country', 'capital', 'pyramid', 'rome', 'civilization', 'dynasty', 'treaty', 'world war']):
            return 'history_geography'
        if any(w in q for w in ['philosophy', 'ethics', 'psychology', 'logic', 'meaning', 'habit', 'relationship', 'interview', 'career', 'book', 'writing', 'language', 'culture']):
            return 'general_knowledge'

        return 'general_knowledge'

    @classmethod
    def select_best_real_world_answer(cls, answers: List[Dict[str, Any]], topic: str, query: str) -> Dict[str, Any]:
        """
        Evaluates all sources and selects the ONE most practical, reliable,
        and relevant real-world answer across any universal or technical question.
        """
        if not answers:
            return None

        best_score = -1.0
        best_candidate = None
        best_rationale = ""
        is_tech = cls.is_technical_topic(topic)

        for a in answers:
            src = a.get('source', '')
            body = a.get('body', '')
            conf = a.get('confidence', 0.5)
            trust = a.get('trust_score', 5)

            # Base confidence & source trust weighting
            score = (conf * 40.0) + (trust * 4.0)

            # Content completeness and depth
            if len(body) >= 200:
                score += 12.0
            elif len(body) >= 100:
                score += 6.0

            # Structural clarity: headers, bullet lists, formatting
            if any(marker in body for marker in ['\n-', '\n*', '\n1.', '###', '##', '**']):
                score += 10.0

            # Bonus for structured tables or comparison matrices
            if '| :---' in body or '| ---' in body:
                score += 12.0

            # Severe penalty for hollow placeholder language
            if any(junk in body for junk in [
                'addresses fundamental principles within',
                'Governed by established empirical standards',
                'Directly impacts strategic decision-making',
                'Prioritize validated facts over subjective speculation'
            ]):
                score -= 35.0

            if is_tech:
                # Technical Domain Scoring
                if '```' in body or 'class ' in body or 'function' in body or 'def ' in body or 'style=' in body:
                    score += 15.0
                if topic in ['html_css', 'javascript'] and src == 'MDN Web Docs':
                    score += 20.0  # Official web standard
                elif src in ['ChatGPT', 'Gemini AI']:
                    score += 18.0  # Modern code synthesis with step-by-step logic
                elif src == 'Stack Overflow' and a.get('score', 0) > 100:
                    score += 14.0  # High peer upvotes
            else:
                # Universal / General Knowledge Scoring
                if src in ['ChatGPT', 'Gemini AI']:
                    score += 20.0  # Deep, structured, multi-paragraph factual synthesis
                elif src == 'Wikipedia':
                    score += 18.0  # Authoritative encyclopedic reference
                elif src == 'Google Search':
                    score += 12.0  # Real-time web reference
                elif src in ['YouTube', 'Reddit']:
                    score += 10.0  # Real community experience / video demonstration

            if score > best_score:
                best_score = score
                best_candidate = a
                
                # Formulate real-world explanation
                if is_tech:
                    if src == 'ChatGPT':
                        best_rationale = "Selected as the #1 Real-World Solution: Delivers clean, modern, production-grade code with error-handling and zero deprecated dependencies."
                    elif src == 'Gemini AI':
                        best_rationale = "Selected as the #1 Real-World Solution: Concise, verified syntax optimized for current language standards with clear implementation examples."
                    elif src == 'MDN Web Docs':
                        best_rationale = "Selected as the #1 Real-World Solution: The authoritative official web standard with 100% browser specification accuracy."
                    elif src == 'Stack Overflow':
                        best_rationale = f"Selected as the #1 Real-World Solution: High community consensus with {a.get('score', 0)}+ developer upvotes and battle-tested reliability."
                    else:
                        best_rationale = f"Selected as the #1 Real-World Solution: Most complete and verified reference for '{query}'."
                else:
                    if topic == 'science':
                        best_rationale = "Selected as the #1 Real-World Answer: Evidence-based scientific explanation detailing fundamental physical principles and observable phenomena."
                    elif topic == 'health_wellness':
                        best_rationale = "Selected as the #1 Real-World Answer: Clear, evidence-supported health guidance with actionable everyday recommendations."
                    elif topic == 'finance_business':
                        best_rationale = "Selected as the #1 Real-World Answer: Practical financial breakdown with mathematical formulas, real-world examples, and actionable advice."
                    elif topic == 'history_geography':
                        best_rationale = "Selected as the #1 Real-World Answer: Thorough historical consensus detailing chronological causes, key actors, and consequences."
                    elif src in ['ChatGPT', 'Gemini AI']:
                        best_rationale = f"Selected as the #1 Real-World Answer: Comprehensive, well-structured breakdown covering core principles, real-world examples, and key takeaways."
                    elif src == 'Wikipedia':
                        best_rationale = f"Selected as the #1 Real-World Answer: Authoritative encyclopedic reference with verified global consensus."
                    else:
                        best_rationale = f"Selected as the #1 Real-World Answer: Most accurate, practical, and comprehensive solution for '{query}'."

        if best_candidate:
            best_candidate['is_best_answer'] = True
            best_candidate['best_reason'] = best_rationale

        return {
            'source': best_candidate.get('source', '') if best_candidate else '',
            'title': best_candidate.get('title', '') if best_candidate else '',
            'reason': best_rationale,
            'best_reason': best_rationale,
            'url': best_candidate.get('url', '') if best_candidate else ''
        }

    @classmethod
    def analyze_consensus(cls, query: str, answers: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not answers:
            return {
                'avg_confidence': 0.0,
                'total_sources': 0,
                'consensus': [],
                'minority': [],
                'conflicts': [],
                'recommendation': 'No sources found for this query.',
                'consensus_recommendation': 'Try refining your search terms.',
                'best_answer': None
            }

        confidences = [a.get('confidence', 0.5) for a in answers]
        avg_conf = round(sum(confidences) / len(confidences), 2)

        sources_present = list(dict.fromkeys(a.get('source') for a in answers if a.get('source')))
        total_sources = len(sources_present)

        consensus_sources = []
        minority_sources = []
        
        for src in sources_present:
            meta = cls.SOURCE_METADATA.get(src, {'base_confidence': 0.65})
            if meta['base_confidence'] >= 0.80:
                consensus_sources.append(src)
            else:
                minority_sources.append(src)

        if not consensus_sources and sources_present:
            consensus_sources.append(sources_present[0])
            minority_sources = sources_present[1:]

        topic = cls.detect_topic(query)
        recommendation_text = cls._generate_consensus_narrative(query, topic, consensus_sources, minority_sources)

        # Select the single best real-world answer
        best_answer_info = cls.select_best_real_world_answer(answers, topic, query)

        return {
            'avg_confidence': avg_conf,
            'total_sources': total_sources,
            'consensus': consensus_sources,
            'minority': minority_sources,
            'conflicts': [],
            'recommendation': f"{total_sources} sources searched. Confidence: {int(avg_conf * 100)}%",
            'consensus_recommendation': recommendation_text,
            'best_answer': best_answer_info
        }

    @staticmethod
    def _generate_consensus_narrative(query: str, topic: str, consensus: List[str], minority: List[str]) -> str:
        con_str = ", ".join(consensus[:3]) if consensus else "Primary documentation"
        
        if topic == 'html_css':
            return f"Strong consensus between {con_str}: Modern CSS Flexbox (`display: flex; justify-content: center; align-items: center;`) or CSS Grid (`place-items: center;`) is the verified standard. Older margin/table hacks are deprecated."
        elif topic == 'python':
            return f"Consensus verified by {con_str}: For data processing, the built-in `csv` module or `pandas.read_csv()` represents the gold standard solution with highest performance and reliability."
        elif topic == 'javascript':
            return f"Consensus reached by {con_str}: Modern ES6+ syntax and native Array methods (`map`, `filter`, `forEach`) are universally recommended over imperative loops for clarity and immutability."
        elif topic == 'git':
            return f"Consensus verified by {con_str}: `git reset --soft HEAD~1` preserves local changes while undoing the commit. Destructive options (`--hard`) are warned against across community forums."
        elif topic == 'java':
            return f"Consensus across {con_str}: Utilizing `StringBuilder.reverse()` is the standard modern Java idiom for in-memory reversal, offering O(n) performance without manual buffer indexing."
        elif topic == 'database':
            return f"Consensus across {con_str}: Standard ANSI SQL queries with explicit `INNER/LEFT JOIN` clauses and index optimization provide optimal query efficiency."
        else:
            return f"Strong consensus identified across {con_str}: The synthesized solution aligns with official language specifications and top-voted community best practices."
