import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyperclip
import json
import os
import threading
from datetime import datetime

# Use translate library instead of googletrans
try:
    from translate import Translator

    TRANSLATOR_AVAILABLE = True
except ImportError:
    messagebox.showerror("Error", "Please install translate library:\n\nRun in terminal: pip install translate")
    TRANSLATOR_AVAILABLE = False
    exit()


class EnhancedTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Translator Pro")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2C3E50")

        # Set minimum window size
        self.root.minsize(900, 650)

        # Center the window
        self.center_window()

        # Load custom fonts
        self.load_fonts()

        # Initialize translator
        self.translator = None
        self.translation_in_progress = False

        # Language options - Common languages with their codes
        self.languages = {
            'en': 'english', 'es': 'spanish', 'fr': 'french', 'de': 'german',
            'it': 'italian', 'pt': 'portuguese', 'ru': 'russian', 'zh': 'chinese',
            'ja': 'japanese', 'ko': 'korean', 'ar': 'arabic', 'hi': 'hindi',
            'pa': 'punjabi', 'bn': 'bengali', 'te': 'telugu', 'mr': 'marathi',
            'ta': 'tamil', 'ur': 'urdu', 'gu': 'gujarati', 'kn': 'kannada',
            'ml': 'malayalam', 'or': 'odia', 'ne': 'nepali', 'si': 'sinhala',
            'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'hy': 'armenian',
            'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bs': 'bosnian',
            'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa',
            'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish',
            'nl': 'dutch', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino',
            'fi': 'finnish', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian',
            'el': 'greek', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian',
            'iw': 'hebrew', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic',
            'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'jw': 'javanese',
            'kk': 'kazakh', 'km': 'khmer', 'rw': 'kinyarwanda', 'ky': 'kirghiz',
            'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian',
            'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy',
            'ms': 'malay', 'mt': 'maltese', 'mi': 'maori', 'mn': 'mongolian',
            'my': 'myanmar', 'no': 'norwegian', 'ps': 'pashto', 'fa': 'persian',
            'pl': 'polish', 'ro': 'romanian', 'sm': 'samoan', 'gd': 'scots gaelic',
            'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi',
            'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'su': 'sundanese',
            'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'th': 'thai',
            'tr': 'turkish', 'uk': 'ukrainian', 'uz': 'uzbek', 'vi': 'vietnamese',
            'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu'
        }

        self.language_codes = list(self.languages.keys())
        self.language_names = list(self.languages.values())

        # Favorites languages
        self.favorites = ['en', 'es', 'fr', 'de', 'it', 'zh', 'ja', 'hi', 'pa']

        # Translation modes
        self.translation_modes = [
            ("Standard Translation", "Balanced speed and accuracy"),
            ("Fast Translation", "Quick but less accurate"),
            ("Accurate Translation", "Slower but more precise")
        ]

        # Stats
        self.translation_count = 0
        self.total_chars_translated = 0

        # History file
        self.history_file = "translation_history.json"
        self.stats_file = "translation_stats.json"
        self.favorites_file = "favorites.json"

        # Load data
        self.history = self.load_history()
        self.stats = self.load_stats()
        self.favorites = self.load_favorites()

        # Default languages
        self.source_lang = "en"
        self.target_lang = "es"

        # Setup UI
        self.setup_ui()

        # Bind keyboard shortcuts
        self.setup_keyboard_shortcuts()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def load_fonts(self):
        """Load custom fonts"""
        self.title_font = ("Segoe UI", 28, "bold")
        self.subtitle_font = ("Segoe UI", 12)
        self.button_font = ("Segoe UI", 11)
        self.text_font = ("Consolas", 11)

    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-t>', lambda e: self.translate_text())
        self.root.bind('<Control-c>', lambda e: self.copy_translation())
        self.root.bind('<Control-l>', lambda e: self.clear_text())
        self.root.bind('<Control-s>', lambda e: self.swap_languages())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-h>', lambda e: self.show_help())

    def setup_ui(self):
        # Main container with gradient effect
        main_container = tk.Frame(self.root, bg="#2C3E50")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_container, bg="#2C3E50")
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Title with icon
        title_frame = tk.Frame(header_frame, bg="#2C3E50")
        title_frame.pack()

        tk.Label(title_frame, text="🌐", font=("Segoe UI", 36), bg="#2C3E50", fg="#3498DB").pack(side=tk.LEFT)
        tk.Label(title_frame, text="AI Translator Pro", font=self.title_font,
                 bg="#2C3E50", fg="white").pack(side=tk.LEFT, padx=10)

        tk.Label(header_frame, text="Translate text between 100+ languages instantly",
                 font=self.subtitle_font, bg="#2C3E50", fg="#BDC3C7").pack()

        # Main content area
        content_frame = tk.Frame(main_container, bg="#34495E")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel
        left_panel = tk.Frame(content_frame, bg="#34495E")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Right panel
        right_panel = tk.Frame(content_frame, bg="#34495E")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Language selection panel
        lang_panel = tk.Frame(left_panel, bg="#34495E")
        lang_panel.pack(fill=tk.X, pady=(0, 15))

        # Source language
        lang_frame = tk.Frame(lang_panel, bg="#34495E")
        lang_frame.pack(fill=tk.X, pady=5)

        tk.Label(lang_frame, text="Source Language:", font=("Segoe UI", 11, "bold"),
                 bg="#34495E", fg="white").pack(anchor="w")

        self.source_combo = ttk.Combobox(
            lang_frame,
            values=sorted(self.language_names),
            width=30,
            font=("Segoe UI", 10),
            state="readonly"
        )
        self.source_combo.pack(fill=tk.X, pady=5)
        self.source_combo.set("english")

        # Target language
        tk.Label(lang_frame, text="Target Language:", font=("Segoe UI", 11, "bold"),
                 bg="#34495E", fg="white").pack(anchor="w", pady=(10, 0))

        self.target_combo = ttk.Combobox(
            lang_frame,
            values=sorted(self.language_names),
            width=30,
            font=("Segoe UI", 10),
            state="readonly"
        )
        self.target_combo.pack(fill=tk.X, pady=5)
        self.target_combo.set("spanish")

        # Quick actions frame
        quick_frame = tk.Frame(lang_frame, bg="#34495E")
        quick_frame.pack(fill=tk.X, pady=10)

        # Swap button
        swap_btn = tk.Button(
            quick_frame,
            text="↻ Swap Languages (Ctrl+S)",
            command=self.swap_languages,
            font=self.button_font,
            bg="#3498DB",
            fg="white",
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        swap_btn.pack(side=tk.LEFT)

        # Input text area
        input_frame = tk.Frame(left_panel, bg="#34495E")
        input_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(input_frame, text="Enter Text to Translate:", font=("Segoe UI", 11, "bold"),
                 bg="#34495E", fg="white").pack(anchor="w")

        input_container = tk.Frame(input_frame, bg="#2C3E50", relief=tk.SUNKEN, borderwidth=1)
        input_container.pack(fill=tk.BOTH, expand=True, pady=5)

        self.input_text = scrolledtext.ScrolledText(
            input_container,
            height=12,
            font=self.text_font,
            wrap=tk.WORD,
            bg="#1C2833",
            fg="#ECF0F1",
            insertbackground="white",
            selectbackground="#3498DB",
            relief=tk.FLAT
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Add sample text
        sample_text = """Hello! Welcome to AI Translator Pro.

This powerful tool can translate text between 100+ languages instantly.

Try translating this text to Spanish or any other language of your choice!"""
        self.input_text.insert("1.0", sample_text)

        # Input stats
        self.input_stats = tk.Label(input_container, text="Characters: 0 | Words: 0",
                                    font=("Segoe UI", 9), bg="#1C2833", fg="#BDC3C7")
        self.input_stats.pack(anchor="se", padx=5, pady=2)
        self.input_text.bind('<KeyRelease>', self.update_input_stats)

        # Output text area
        output_frame = tk.Frame(right_panel, bg="#34495E")
        output_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(output_frame, text="Translated Text:", font=("Segoe UI", 11, "bold"),
                 bg="#34495E", fg="white").pack(anchor="w")

        output_container = tk.Frame(output_frame, bg="#2C3E50", relief=tk.SUNKEN, borderwidth=1)
        output_container.pack(fill=tk.BOTH, expand=True, pady=5)

        self.output_text = scrolledtext.ScrolledText(
            output_container,
            height=12,
            font=self.text_font,
            wrap=tk.WORD,
            bg="#1C2833",
            fg="#ECF0F1",
            state=tk.DISABLED,
            relief=tk.FLAT
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Output stats
        self.output_stats = tk.Label(output_container, text="Translation ready", font=("Segoe UI", 9),
                                     bg="#1C2833", fg="#BDC3C7")
        self.output_stats.pack(anchor="se", padx=5, pady=2)

        # Action buttons
        button_frame = tk.Frame(main_container, bg="#2C3E50")
        button_frame.pack(fill=tk.X, pady=15)

        # Translate button
        self.translate_btn = tk.Button(
            button_frame,
            text="🚀 Translate (Ctrl+T)",
            command=self.translate_text,
            font=("Segoe UI", 12, "bold"),
            bg="#2ECC71",
            fg="white",
            padx=25,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.translate_btn.pack(side=tk.LEFT, padx=5)

        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear All (Ctrl+L)",
            command=self.clear_text,
            font=self.button_font,
            bg="#E74C3C",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Copy button
        copy_btn = tk.Button(
            button_frame,
            text="📋 Copy (Ctrl+C)",
            command=self.copy_translation,
            font=self.button_font,
            bg="#3498DB",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        copy_btn.pack(side=tk.LEFT, padx=5)

        # Save button
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Translation",
            command=self.save_translation,
            font=self.button_font,
            bg="#F39C12",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=5)

        # Bottom panel
        bottom_panel = tk.Frame(main_container, bg="#2C3E50")
        bottom_panel.pack(fill=tk.X, pady=(10, 0))

        # History section
        history_frame = tk.Frame(bottom_panel, bg="#34495E")
        history_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(history_frame, text="📜 Recent Translations", font=("Segoe UI", 11, "bold"),
                 bg="#34495E", fg="white").pack(anchor="w")

        history_btn_frame = tk.Frame(history_frame, bg="#34495E")
        history_btn_frame.pack(fill=tk.X, pady=5)

        tk.Button(
            history_btn_frame,
            text="Load Selected",
            command=self.load_from_history,
            font=("Segoe UI", 9),
            bg="#FF9800",
            fg="white",
            padx=10,
            pady=3,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            history_btn_frame,
            text="Clear History",
            command=self.clear_history,
            font=("Segoe UI", 9),
            bg="#95A5A6",
            fg="white",
            padx=10,
            pady=3,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)

        self.history_listbox = tk.Listbox(
            history_frame,
            height=6,
            font=("Segoe UI", 9),
            bg="#1C2833",
            fg="#ECF0F1",
            selectbackground="#3498DB",
            relief=tk.FLAT
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Stats section
        stats_frame = tk.Frame(bottom_panel, bg="#34495E")
        stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(stats_frame, text="📊 Translation Stats", font=("Segoe UI", 11, "bold"),
                 bg="#34495E", fg="white").pack(anchor="w")

        stats_text = tk.Text(
            stats_frame,
            height=6,
            font=("Segoe UI", 9),
            bg="#1C2833",
            fg="#ECF0F1",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        stats_text.pack(fill=tk.BOTH, expand=True, pady=5)

        self.update_stats_display(stats_text)

        # Status bar
        self.status_bar = tk.Label(
            main_container,
            text="✅ Ready - AI Translator Pro v1.0 | Press Ctrl+T to Translate | Ctrl+H for Help",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#1C2833",
            fg="#2ECC71",
            font=("Segoe UI", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        # Load history into listbox
        self.update_history_listbox()

        # Add context menu
        self.setup_context_menu()

    def setup_context_menu(self):
        """Setup right-click context menu"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_selection)
        self.context_menu.add_command(label="Paste", command=self.paste_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=self.select_all)

        self.input_text.bind("<Button-3>", self.show_context_menu)
        self.output_text.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        """Show context menu on right-click"""
        self.context_menu.post(event.x_root, event.y_root)

    def copy_selection(self):
        """Copy selected text"""
        try:
            selected_text = self.root.clipboard_get()
            if selected_text:
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
        except:
            pass

    def paste_text(self):
        """Paste text"""
        try:
            clipboard_text = self.root.clipboard_get()
            if clipboard_text:
                self.input_text.insert(tk.INSERT, clipboard_text)
        except:
            pass

    def select_all(self):
        """Select all text in focused widget"""
        widget = self.root.focus_get()
        if widget == self.input_text:
            self.input_text.tag_add(tk.SEL, "1.0", tk.END)
        elif widget == self.output_text:
            self.output_text.tag_add(tk.SEL, "1.0", tk.END)

    def update_input_stats(self, event=None):
        """Update input character count"""
        text = self.input_text.get("1.0", tk.END).strip()
        char_count = len(text)
        word_count = len(text.split())
        self.input_stats.config(text=f"Characters: {char_count} | Words: {word_count}")

    def update_stats_display(self, stats_text):
        """Update statistics display"""
        stats_text.config(state=tk.NORMAL)
        stats_text.delete("1.0", tk.END)

        total_translations = self.stats.get('total_translations', 0)
        total_chars = self.stats.get('total_chars', 0)
        today_date = datetime.now().strftime("%Y-%m-%d")

        stats_info = f"""
Total Translations: {total_translations}
Characters Translated: {total_chars:,}
Today's Date: {today_date}
Most Used Language: {self.stats.get('most_used_lang', 'English')}

Tip: Use Ctrl+T for quick translation!
"""
        stats_text.insert("1.0", stats_info)
        stats_text.config(state=tk.DISABLED)

    def get_language_code(self, language_name):
        """Convert language name to language code"""
        for code, name in self.languages.items():
            if name.lower() == language_name.lower():
                return code
        return "en"

    def translate_text(self):
        """Translate the input text in a separate thread"""
        if self.translation_in_progress:
            return

        # Get text from input
        text_to_translate = self.input_text.get("1.0", tk.END).strip()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return

        # Get selected languages
        source_lang_name = self.source_combo.get()
        target_lang_name = self.target_combo.get()

        source_lang_code = self.get_language_code(source_lang_name)
        target_lang_code = self.get_language_code(target_lang_name)

        # Update status
        self.status_bar.config(text="🔄 Translating... Please wait")
        self.translate_btn.config(state=tk.DISABLED, text="Translating...")
        self.translation_in_progress = True

        # Start translation in separate thread
        thread = threading.Thread(
            target=self.perform_translation,
            args=(text_to_translate, source_lang_code, target_lang_code, source_lang_name, target_lang_name)
        )
        thread.daemon = True
        thread.start()

    def perform_translation(self, text_to_translate, src_code, dest_code, src_name, dest_name):
        """Perform translation in background thread"""
        try:
            # Create translator and translate
            self.translator = Translator(from_lang=src_code, to_lang=dest_code)
            translation = self.translator.translate(text_to_translate)

            # Update UI in main thread
            self.root.after(0, self.update_translation_result,
                            translation, text_to_translate, src_name, dest_name)

        except Exception as e:
            self.root.after(0, self.translation_error, str(e))

    def update_translation_result(self, translation, original, src_name, dest_name):
        """Update UI with translation result"""
        # Display translation
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", translation)
        self.output_text.config(state=tk.DISABLED)

        # Update output stats
        char_count = len(translation)
        word_count = len(translation.split())
        self.output_stats.config(text=f"Characters: {char_count} | Words: {word_count}")

        # Save to history
        self.save_to_history(original, translation, src_name, dest_name)

        # Update stats
        self.update_stats(original)

        # Reset UI
        self.translate_btn.config(state=tk.NORMAL, text="🚀 Translate (Ctrl+T)")
        self.status_bar.config(text=f"✅ Translated from {src_name} to {dest_name}")
        self.translation_in_progress = False

    def translation_error(self, error_msg):
        """Handle translation error"""
        messagebox.showerror("Translation Error",
                             f"An error occurred:\n\n{error_msg}\n\nPlease check your internet connection.")
        self.status_bar.config(text="❌ Translation failed")
        self.translate_btn.config(state=tk.NORMAL, text="🚀 Translate (Ctrl+T)")
        self.translation_in_progress = False

    def update_stats(self, text):
        """Update translation statistics"""
        self.translation_count += 1
        self.total_chars_translated += len(text)

        self.stats['total_translations'] = self.stats.get('total_translations', 0) + 1
        self.stats['total_chars'] = self.stats.get('total_chars', 0) + len(text)

        # Save stats
        self.save_stats()

    def swap_languages(self):
        """Swap source and target languages"""
        source = self.source_combo.get()
        target = self.target_combo.get()

        self.source_combo.set(target)
        self.target_combo.set(source)

        # Also swap the text if there's content
        if self.input_text.get("1.0", tk.END).strip() and self.output_text.get("1.0", tk.END).strip():
            input_text = self.input_text.get("1.0", tk.END)
            output_text = self.output_text.get("1.0", tk.END)

            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", output_text)

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", input_text)
            self.output_text.config(state=tk.DISABLED)

        self.status_bar.config(text="🔄 Languages swapped")

    def clear_text(self):
        """Clear input and output text areas"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.input_stats.config(text="Characters: 0 | Words: 0")
        self.output_stats.config(text="Translation cleared")
        self.status_bar.config(text="🗑️ Text cleared")

    def copy_translation(self):
        """Copy translation to clipboard"""
        translation = self.output_text.get("1.0", tk.END).strip()
        if translation:
            try:
                pyperclip.copy(translation)
                self.status_bar.config(text="📋 Translation copied to clipboard")
                # Flash effect
                original_bg = self.output_text.cget('bg')
                self.output_text.config(bg='#27AE60')
                self.root.after(200, lambda: self.output_text.config(bg=original_bg))
            except:
                self.root.clipboard_clear()
                self.root.clipboard_append(translation)
                self.status_bar.config(text="📋 Translation copied to clipboard")
        else:
            messagebox.showinfo("Copy", "No translation to copy")

    def save_translation(self):
        """Save translation to file"""
        original = self.input_text.get("1.0", tk.END).strip()
        translated = self.output_text.get("1.0", tk.END).strip()

        if not translated:
            messagebox.showwarning("Save Error", "No translation to save.")
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"translation_{timestamp}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Original Text ({self.source_combo.get()}):\n")
                f.write("=" * 50 + "\n")
                f.write(original + "\n\n")
                f.write(f"Translated Text ({self.target_combo.get()}):\n")
                f.write("=" * 50 + "\n")
                f.write(translated + "\n\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            self.status_bar.config(text=f"💾 Translation saved as {filename}")
            messagebox.showinfo("Success", f"Translation saved to:\n{filename}")

        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save: {str(e)}")

    def show_help(self):
        """Show help information"""
        help_text = """
AI Translator Pro - Help Guide

Shortcuts:
Ctrl+T - Translate text
Ctrl+C - Copy translation
Ctrl+L - Clear all text
Ctrl+S - Swap languages
Ctrl+H - Show this help
Ctrl+Q - Quit application

Features:
• Translate between 100+ languages
• Save translations to file
• Translation history
• Character/word count
• Dark mode interface

Tips:
• Right-click for context menu
• Use swap button to quickly reverse languages
• Save important translations
• Check translation history for recent translations
"""
        messagebox.showinfo("Help Guide", help_text)

    def save_to_history(self, original, translated, source_lang, target_lang):
        """Save translation to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = {
            "original": original,
            "translated": translated,
            "source": source_lang,
            "target": target_lang,
            "timestamp": timestamp,
            "char_count": len(original)
        }

        # Add to beginning of history
        self.history.insert(0, entry)

        # Keep only last 50 translations
        if len(self.history) > 50:
            self.history = self.history[:50]

        # Save to file
        self.save_history()

        # Update listbox
        self.update_history_listbox()

    def load_history(self):
        """Load translation history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        """Save translation history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_stats(self):
        """Load statistics from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_stats(self):
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass

    def load_favorites(self):
        """Load favorite languages from file"""
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, 'r') as f:
                    return json.load(f)
            except:
                return ['en', 'es', 'fr', 'de', 'it', 'zh', 'ja', 'hi', 'pa']
        return ['en', 'es', 'fr', 'de', 'it', 'zh', 'ja', 'hi', 'pa']

    def update_history_listbox(self):
        """Update the history listbox with recent translations"""
        self.history_listbox.delete(0, tk.END)

        for entry in self.history[:15]:  # Show only last 15
            timestamp = entry.get('timestamp', '')
            display_text = f"[{timestamp}] {entry['source']} → {entry['target']}: {entry['original'][:40]}..."
            self.history_listbox.insert(tk.END, display_text)

    def load_from_history(self):
        """Load selected translation from history"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showinfo("Selection", "Please select a translation from history")
            return

        index = selection[0]
        if index < len(self.history):
            entry = self.history[index]

            # Set languages
            self.source_combo.set(entry['source'])
            self.target_combo.set(entry['target'])

            # Set text
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", entry['original'])

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", entry['translated'])
            self.output_text.config(state=tk.DISABLED)

            self.status_bar.config(text=f"📜 Loaded translation from {entry.get('timestamp', 'history')}")

    def clear_history(self):
        """Clear translation history"""
        if messagebox.askyesno("Clear History",
                               "Are you sure you want to clear all translation history?\nThis action cannot be undone."):
            self.history = []
            self.save_history()
            self.update_history_listbox()
            self.status_bar.config(text="🗑️ History cleared")


def main():
    root = tk.Tk()
    app = EnhancedTranslatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()