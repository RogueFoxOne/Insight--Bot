#!/usr/bin/env python3
"""
AI Coding Assistant - FREE-FIRST Edition
Zero-cost operation with HuggingFace & Ollama priority
"""

import os
import sys
import json
import re
from typing import Optional, Dict, List, Any
from datetime import datetime
from pathlib import Path
import readline

# Configuration
class Config:
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    FREE_MODELS = {
        'huggingface': 'mistralai/Mixtral-8x7B-Instruct-v0.1',
        'ollama': 'codellama:13b',
    }
    
    PAID_FALLBACK_MODELS = {
        'groq': 'llama-3.1-70b-versatile',
        'anthropic': 'claude-3-5-sonnet-20240620', # Updated model name for best compatibility
        'openai': 'gpt-4o'
    }
    
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7
    MAX_FILE_SIZE = 100000
    SUPPORTED_EXTENSIONS = ['.py', '.js', '.jsx', '.ts', '.tsx', '.css', '.html', '.json', '.md']
    PLK_ENABLED = True
    ADHD_MODE = True
    MAX_HISTORY = 10
    HISTORY_FILE = Path.home() / '.ai_coding_assistant_history.json'

# AI Providers
class AIProvider:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
    
    def generate(self, prompt: str, system: str = "", **kwargs) -> str:
        raise NotImplementedError

class HuggingFaceProvider(AIProvider):
    def generate(self, prompt: str, system: str = "", **kwargs) -> str:
        try:
            import requests
            import time
            
            model = Config.FREE_MODELS['huggingface']
            url = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            full_prompt = f"{system}\n\n{prompt}" if system else prompt
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": kwargs.get('max_tokens', Config.MAX_TOKENS),
                    "temperature": kwargs.get('temperature', Config.TEMPERATURE),
                    "return_full_text": False
                }
            }
            
            # ENHANCED: Retry logic for HuggingFace model loading
            for attempt in range(3):
                response = requests.post(url, headers=headers, json=payload, timeout=45)
                if response.status_code != 503:
                    break
                print(f" (model loading, retrying in 15s...)", end='', flush=True)
                time.sleep(15)
            
            response.raise_for_status()
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '')
            elif isinstance(result, dict):
                return result.get('generated_text', '')
            else:
                return str(result)
                
        except Exception as e:
            raise Exception(f"HuggingFace API error: {str(e)}")

class OllamaProvider(AIProvider):
    def __init__(self):
        super().__init__("")
    
    def generate(self, prompt: str, system: str = "", **kwargs) -> str:
        try:
            import requests
            
            url = f"{Config.OLLAMA_BASE_URL}/api/generate"
            
            payload = {
                "model": Config.FREE_MODELS['ollama'],
                "prompt": prompt,
                "system": system,
                "stream": False,
                "options": {
                    "temperature": kwargs.get('temperature', Config.TEMPERATURE),
                    "num_predict": kwargs.get('max_tokens', Config.MAX_TOKENS)
                }
            }
            
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            return response.json().get('response', '')
            
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}. Is Ollama running? Try: ollama serve")

class GroqProvider(AIProvider):
    def generate(self, prompt: str, system: str = "", **kwargs) -> str:
        try:
            from groq import Groq
            
            client = Groq(api_key=self.api_key)
            
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model=Config.PAID_FALLBACK_MODELS['groq'],
                messages=messages,
                max_tokens=kwargs.get('max_tokens', Config.MAX_TOKENS),
                temperature=kwargs.get('temperature', Config.TEMPERATURE)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

class AnthropicProvider(AIProvider):
    def generate(self, prompt: str, system: str = "", **kwargs) -> str:
        try:
            from anthropic import Anthropic
            
            client = Anthropic(api_key=self.api_key)
            messages = [{"role": "user", "content": prompt}]
            
            response = client.messages.create(
                model=Config.PAID_FALLBACK_MODELS['anthropic'],
                max_tokens=kwargs.get('max_tokens', Config.MAX_TOKENS),
                temperature=kwargs.get('temperature', Config.TEMPERATURE),
                system=system,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

class OpenAIProvider(AIProvider):
    def generate(self, prompt: str, system: str = "", **kwargs) -> str:
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model=Config.PAID_FALLBACK_MODELS['openai'],
                messages=messages,
                max_tokens=kwargs.get('max_tokens', Config.MAX_TOKENS),
                temperature=kwargs.get('temperature', Config.TEMPERATURE)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

# AI Router
class AIRouter:
    def __init__(self):
        self.providers = []
        self._initialize_providers()
    
    def _initialize_providers(self):
        print("🔍 Initializing AI providers (FREE FIRST)...")
        print("=" * 60)
        
        if Config.HUGGINGFACE_API_KEY:
            try:
                self.providers.append(('🆓 HuggingFace Mixtral', HuggingFaceProvider(Config.HUGGINGFACE_API_KEY)))
                print("✅ HuggingFace Inference API (FREE tier)")
            except ImportError:
                print("⚠️  requests library needed: pip install requests")
        else:
            print("💡 Get FREE HuggingFace key: https://huggingface.co/settings/tokens")
        
        try:
            import requests
            try:
                test_response = requests.get(Config.OLLAMA_BASE_URL, timeout=2)
                if test_response.status_code == 200:
                    self.providers.append(('🆓 Ollama CodeLlama (LOCAL)', OllamaProvider()))
                    print("✅ Ollama (100% FREE & LOCAL)")
                else:
                    print("💡 Ollama available but returned non-200 status.")
            except requests.exceptions.RequestException:
                print("💡 Install Ollama for FREE local AI: https://ollama.ai")
        except ImportError:
            print("⚠️  requests library needed: pip install requests")
        
        if Config.GROQ_API_KEY:
            try:
                self.providers.append(('🆓 Groq Llama (Free tier)', GroqProvider(Config.GROQ_API_KEY)))
                print("✅ Groq (Generous FREE tier)")
            except ImportError:
                print("⚠️  Groq library needed: pip install groq")
        else:
            print("💡 Get FREE Groq key: https://console.groq.com")
        
        if Config.ANTHROPIC_API_KEY:
            try:
                self.providers.append(('💰 Anthropic Claude', AnthropicProvider(Config.ANTHROPIC_API_KEY)))
                print("✅ Anthropic Claude (PAID fallback)")
            except ImportError:
                print("⚠️  Anthropic library needed: pip install anthropic")
        
        if Config.OPENAI_API_KEY:
            try:
                self.providers.append(('💰 OpenAI GPT-4o', OpenAIProvider(Config.OPENAI_API_KEY)))
                print("✅ OpenAI GPT-4o (PAID fallback)")
            except ImportError:
                print("⚠️  OpenAI library needed: pip install openai")
        
        print("=" * 60)
        
        if not self.providers:
            print("\n❌ NO AI PROVIDERS AVAILABLE!")
            print("\n🆓 FREE OPTIONS (Recommended):")
            print("1. HuggingFace (FREE API):")
            print("   export HUGGINGFACE_API_KEY='your-free-key'")
            print("   Get key: https://huggingface.co/settings/tokens")
            print("\n2. Ollama (100% LOCAL/FREE):")
            print("   Install: https://ollama.ai")
            print("   Run: ollama pull codellama && ollama serve")
            sys.exit(1)
        
        free_count = sum(1 for name, _ in self.providers if '🆓' in name)
        paid_count = sum(1 for name, _ in self.providers if '💰' in name)
        print(f"\n✨ Loaded {free_count} FREE and {paid_count} PAID providers\n")
    
    def generate(self, prompt: str, system: str = "", **kwargs) -> Dict[str, Any]:
        for name, provider in self.providers:
            try:
                print(f"🤖 Using {name}...", end='', flush=True)
                response = provider.generate(prompt, system, **kwargs)
                if not response or not response.strip():
                    raise ValueError("Empty response received")
                print(" ✅")
                
                if '🆓' in name:
                    print("💰 Cost: FREE! ✨")
                else:
                    print("💰 Cost: PAID (fallback)")
                
                return {
                    'success': True,
                    'provider': name,
                    'response': response,
                    'free': '🆓' in name
                }
            except Exception as e:
                print(f" ❌ ({str(e)[:50]}...)")
                continue
        
        return {
            'success': False,
            'provider': 'None',
            'response': 'All AI providers failed. Check your API keys, internet connection, and local Ollama server.',
            'free': False
        }

# PLK Engine
class PLKEngine:
    @staticmethod
    def enhance_prompt(prompt: str) -> str:
        if not Config.PLK_ENABLED:
            return prompt
        
        plk_context = (
            "\n\n[PLK: Keith, ADHD dev. Visual, empowering, direct style. "
            "Complete code blocks. Celebrate wins. No fragments.]"
        )
        
        return prompt + plk_context
    
    @staticmethod
    def format_adhd_friendly(text: str) -> str:
        if not Config.ADHD_MODE:
            return text
        
        # FIXED: Regex syntax for whitespace was 's+', changed to '\s+'
        # Added newlines for better spacing around headers.
        text = re.sub(r'^(#+\s+.+)$', r'\n\1\n', text, flags=re.MULTILINE)
        
        # FIXED: Used a backreference '\1' to capture the keyword, not a control character.
        text = re.sub(r'(TODO|FIXME|NOTE):', r'**\1:**', text)
        
        return text

# File System
class FileSystem:
    @staticmethod
    def read_file(file_path: str) -> Optional[str]:
        try:
            path = Path(file_path)
            
            if not path.is_file():
                return f"Error: Path is not a file: {file_path}"
            
            if path.stat().st_size > Config.MAX_FILE_SIZE:
                return f"File too large (>{Config.MAX_FILE_SIZE} bytes)"
            
            if path.suffix not in Config.SUPPORTED_EXTENSIONS:
                return f"Unsupported file type: {path.suffix}"
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
                
        except Exception as e:
            return f"Error reading file: {str(e)}"

# Conversation Manager
class ConversationManager:
    def __init__(self):
        self.history: List[Dict] = []
        self.load_history()
    
    def add(self, role: str, content: str):
        self.history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        if len(self.history) > Config.MAX_HISTORY * 2:
            self.history = self.history[-Config.MAX_HISTORY * 2:]
        
        self.save_history()
    
    def get_context(self) -> str:
        if not self.history:
            return ""
        
        recent = self.history[-(Config.MAX_HISTORY // 2):]
        return "\n".join([
            f"{msg['role']}: {msg['content'][:200]}"
            for msg in recent
        ])
    
    def save_history(self):
        try:
            with open(Config.HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2)
        # ENHANCED: More specific exceptions
        except (IOError, TypeError) as e:
            print(f"Warning: Could not save history: {e}", file=sys.stderr)

    def load_history(self):
        try:
            if Config.HISTORY_FILE.exists():
                with open(Config.HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        # ENHANCED: More specific exceptions
        except (IOError, json.JSONDecodeError):
            self.history = []
    
    def clear(self):
        self.history = []
        self.save_history()
        print("Conversation history cleared.")

# Coding Assistant
class CodingAssistant:
    def __init__(self):
        print("🎨 Initializing FREE-FIRST AI Coding Assistant...")
        print("=" * 60)
        
        self.router = AIRouter()
        self.plk = PLKEngine()
        self.fs = FileSystem()
        self.conversation = ConversationManager()
        
        print("=" * 60)
        print("✨ AI Coding Assistant ready!")
        print("Type 'help' for commands, 'exit' to quit\n")
    
    def run(self):
        while True:
            try:
                user_input = input("\n🎯 > ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!\n")
                    break
                
                self.process_command(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Exiting...\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
    
    def process_command(self, command: str):
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        handlers = {
            'help': self.cmd_help,
            'code': lambda: self.cmd_code(args),
            'explain': lambda: self.cmd_explain(args),
            'debug': lambda: self.cmd_debug(args),
            'chat': lambda: self.cmd_chat(args),
            'status': self.cmd_status,
            'clear': self.conversation.clear
        }
        
        handler = handlers.get(cmd)
        
        if handler:
            handler()
        else:
            self.cmd_chat(command)
    
    def cmd_help(self):
        help_text = """
╔══════════════════════════════════════════════════════╗
║      AI CODING ASSISTANT - FREE-FIRST EDITION        ║
╚══════════════════════════════════════════════════════╝

📝 COMMANDS:
  code <description>      Generate code for a given description.
  explain <file_path>     Explain the code in the specified file.
  debug <error>           Get help debugging an error message.
  chat <message>          Have a general conversation with the AI.
  status                  Show available AI providers and system status.
  clear                   Clear the current conversation history.
  help                    Show this help message.
  exit / quit / q         Exit the assistant.

💡 Any input that isn't a command is treated as a 'chat' message.
🆓 Prioritizes FREE providers (HuggingFace & Ollama)!
        """
        print(help_text)
    
    def cmd_code(self, description: str):
        if not description:
            print("❌ Usage: code <description>")
            return
        
        system_prompt = "You are a coding assistant. Generate clean, production-ready code with comments and error handling."
        prompt = self.plk.enhance_prompt(
            f"Generate code for: {description}\n\nConversation Context:\n{self.conversation.get_context()}"
        )
        
        self.conversation.add('user', f"code: {description}")
        result = self.router.generate(prompt, system_prompt)
        
        if result['success']:
            output = self.plk.format_adhd_friendly(result['response'])
            print(f"\n{output}\n")
            self.conversation.add('assistant', output)
        else:
            print(f"\n❌ {result['response']}\n")
    
    def cmd_explain(self, file_path: str):
        if not file_path:
            print("❌ Usage: explain <file>")
            return
        
        content = self.fs.read_file(file_path)
        if content is None or content.startswith("Error:"):
            print(f"❌ Could not read file or error occurred: {content or file_path}")
            return
        
        system_prompt = "Explain code clearly with purpose, components, and key logic."
        
        # FIXED: f-string syntax was broken and content was not being used.
        prompt = self.plk.enhance_prompt(f"""
Explain the following code from the file '{file_path}':

```
{content}
```
        """)
        
        self.conversation.add('user', f"explain: {file_path}")
        result = self.router.generate(prompt, system_prompt)
        
        if result['success']:
            output = self.plk.format_adhd_friendly(result['response'])
            print(f"\n{output}\n")
            self.conversation.add('assistant', output)
        else:
            print(f"\n❌ {result['response']}\n")
    
    def cmd_debug(self, error: str):
        if not error:
            print("❌ Usage: debug <error message>")
            return
        
        system_prompt = "Debug expert. Provide root cause analysis, fix suggestions, code examples, and prevention tips."
        prompt = self.plk.enhance_prompt(
            f"Debug the following error:\n\n{error}\n\nConversation Context:\n{self.conversation.get_context()}"
        )
        
        self.conversation.add('user', f"debug: {error}")
        result = self.router.generate(prompt, system_prompt)
        
        if result['success']:
            output = self.plk.format_adhd_friendly(result['response'])
            print(f"\n{output}\n")
            self.conversation.add('assistant', output)
        else:
            print(f"\n❌ {result['response']}\n")
    
    def cmd_chat(self, message: str):
        if not message:
            return
        
        system_prompt = "You are a consciousness-serving AI coding assistant. Be helpful, empowering, and ADHD-friendly."
        prompt = self.plk.enhance_prompt(
            f"{message}\n\nConversation Context:\n{self.conversation.get_context()}"
        )
        
        self.conversation.add('user', message)
        result = self.router.generate(prompt, system_prompt)
        
        if result['success']:
            output = self.plk.format_adhd_friendly(result['response'])
            print(f"\n{output}\n")
            self.conversation.add('assistant', output)
        else:
            print(f"\n❌ {result['response']}\n")
    
    def cmd_status(self):
        print("\n📊 SYSTEM STATUS")
        print("=" * 60)
        
        free_providers = [name for name, _ in self.router.providers if '🆓' in name]
        paid_providers = [name for name, _ in self.router.providers if '💰' in name]
        
        print(f"🆓 FREE Providers ({len(free_providers)} available):")
        for name in free_providers:
            print(f"   ✅ {name}")
        if not free_providers: print("   (None configured)")
        
        print(f"\n💰 PAID Providers ({len(paid_providers)} available):")
        for name in paid_providers:
            print(f"   ✅ {name}")
        if not paid_providers: print("   (None configured)")
        
        print(f"\n💬 Messages in history: {len(self.conversation.history)}")
        print("=" * 60)

def main():
    banner = """
    ╔═══════════════════════════════════════════════════╗
    ║                                                   ║
    ║    🆓  AI CODING ASSISTANT - FREE-FIRST         ║
    ║                                                   ║
    ║        HuggingFace & Ollama Priority             ║
    ║        Built by Keith Soyka / GestaltView        ║
    ║                                                   ║
    ╚═══════════════════════════════════════════════════╝
    """
    print(banner)
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    try:
        assistant = CodingAssistant()
        assistant.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
