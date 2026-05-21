import streamlit as st

class storage:
    def __init__(self):
        if "saved_files" not in st.session_state:
            st.session_state.saved_files = []
            
    def save_data(self, original_text, results):
        data_dict = {
            "original_text": original_text,
            "analysis_result": results
        }
        st.session_state.saved_files.append(data_dict)
        
    def get_all_data(self):
        return st.session_state.saved_files

class analyzer:
    def __init__(self, text):
        self.text = text
        self.bad_words_db = ["bad", "stupid", "failed", "rejected"]
        self.positive_words = ["good", "excellent", "nice", "wonderful", "great", "hero"]
        self.negative_words = ["sad", "tired", "ugly", "not good", "problem"]
        
    def count_chars(self):
        return len(self.text)

    def count_words(self):
        if self.text.strip() == "":
            return 0
        words_list = self.text.split()
        return len(words_list)

    def count_sentences(self):
        count = self.text.count('.') + self.text.count('!') + self.text.count('?')
        if count == 0 and len(self.text) > 0:
            return 1
        return count

    def get_longest_word(self):
        words = self.text.split()
        if len(words) == 0:
            return "None"
        
        longest = words[0]
        for word in words:
            if len(word) > len(longest):
                longest = word
        return longest

    def find_bad_words(self):
        found_words = []
        words = self.text.split()
        for word in words:
            if word in self.bad_words_db:
                found_words.append(word)
        return found_words

    def analyze_sentiment(self):
        pos_count = 0
        neg_count = 0
        words = self.text.split()
        
        for word in words:
            if word in self.positive_words:
                pos_count += 1
            if word in self.negative_words:
                neg_count += 1
                
        if pos_count > neg_count:
            return "Positive"
        elif neg_count > pos_count:
            return "Negative"
        else:
            return "Neutral (or unknown)"

    def get_full_report(self):
        report = {
            "Character Count": self.count_chars(),
            "Word Count": self.count_words(),
            "Sentence Count": self.count_sentences(),
            "Longest Word": self.get_longest_word(),
            "Found Bad Words": self.find_bad_words(),
            "Sentiment Analysis": self.analyze_sentiment()
        }
        return report

def main():
    st.sidebar.title("MENU")
    sections = ["MAIN PAGE", "TEXT"]
    choice = st.sidebar.selectbox("Choose a section:", sections)

    if choice == "MAIN PAGE":
        st.title("WELCOME TO THE MAIN PAGE")
        st.write("This is the main page of the application. Use the sidebar to navigate to different sections.")
        st.markdown("---")
        st.write("You can analyze text, upload files, and view saved analyses.")
        st.markdown("---")
        st.write("USE THE SIDEBAR TO NAVIGATE TO DIFFERENT SECTIONS.")
        
    elif choice == "TEXT":
        st.title("TEXT ANALYSIS")
        user_input = st.text_area("Enter text to analyze:  ")
        col1, col2 = st.columns(2)
        
        with col1:
            start_button = st.button("START ANALYSIS")
        with col2:
            save_button = st.button("SAVE ANALYSIS") # هنا بعدين من نضيف السكشن مال سيف
            
        if start_button:
            if user_input.strip() != "":
                text_analyzer = analyzer(user_input)
                result = text_analyzer.get_full_report()
                
                st.success("Analysis completed!")
                st.write("### Analysis Result: ")
                st.json(result)
                
                st.session_state.temp_text = user_input
                st.session_state.temp_result = result
            else:
                st.warning("ENTER TEXT FIRST")#بعد السكشنات مال السيف ومال فايل

if __name__ == "__main__":
    main()