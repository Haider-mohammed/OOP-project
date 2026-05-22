import streamlit as st

class storage:
    def __init__(self):
        if "saved_files" not in st.session_state:
            st.session_state.saved_files = []
    def save_data(self, data_type="TEXT", file_name="", original_text="", results=None):
        data_dict = {
            "type": data_type,
            "file_name": file_name,
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
    sections = ["MAIN PAGE", "TEXT", "FILE", "SAVES"]
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
            save_button = st.button("SAVE ANALYSIS") 
            
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
                st.warning("ENTER TEXT FIRST")
        if save_button:
            if "temp_result" in st.session_state and st.session_state.temp_text == user_input:
                db = storage()
                db.save_data(original_text=st.session_state.temp_text, results=st.session_state.temp_result, data_type="TEXT")
                st.success("Analysis saved successfully!")
            elif user_input.strip() == "":
                st.warning("ENTER TEXT FIRST")
            else:
                st.warning("Please analyze the text first before saving!")
    elif choice == "FILE":
        st.title("FILE ANALYSIS")
        st.write("please upload a text file to analyze:")
        uploaded_file = st.file_uploader("Upload a text file (.txt):", type=["txt"])
        co1,co2 = st.columns(2)
        with co1:
            start_button = st.button("START ANALYSIS")
        with co2:
            save_button = st.button("SAVE ANALYSIS")
        if uploaded_file is not None:
            file_content = uploaded_file.read().decode("utf-8")
            if start_button:
                if file_content.strip() != "":
                    file_analyzer = analyzer(file_content)
                    result = file_analyzer.get_full_report()
                    st.success("Analysis completed!")
                    st.write("### Analysis Result: ")
                    st.json(result)
                    st.session_state.temp_file_name = uploaded_file.name
                    st.session_state.temp_file_text = file_content
                    st.session_state.temp_file_result = result
                else:
                    st.warning("THE UPLOADED FILE IS EMPTY!")
        if save_button:
            if "temp_file_result" in st.session_state and uploaded_file is not None:
                if st.session_state.temp_file_name == uploaded_file.name:
                    db = storage()
                    db.save_data(
                        original_text=st.session_state.temp_file_text,
                        results=st.session_state.temp_file_result,
                        data_type="FILE",
                        file_name=st.session_state.temp_file_name
                    )
                    st.success(f"FILE SAVED DONE: {st.session_state.temp_file_name}")
                else:
                    st.warning("PLS CLICK START ANALYSIS FIRST")
            else:
                st.warning("PLS UPLOAD A FILE AND CLICK START ANALYSIS FIRST")
    elif choice == "SAVES":
        st.title("YOUR SAVES")
        db = storage()
        all_saves = db.get_all_data()
        if not all_saves:
            st.info("No saved records found yet! Go to TEXT or ADD FILE sections to save some analyses.")
        else:
            st.write(f"Total saved items: {len(all_saves)}")
            st.markdown("---")
            for idx, item in enumerate(all_saves):
                if item.get("type") == "FILE":
                    box_title = f"File: {item.get('file_name', 'Unknown')}"
                else:
                    box_title = f"Text Analysis #{idx + 1}"
                with st.expander(box_title):
                    st.write("**Original Content:**")
                    st.text_area("Content Preview", item["original_text"], height=100, key=f"saved_txt_{idx}", disabled=True)
                    st.write("**Analysis Results:**")
                    st.json(item["analysis_result"])
if __name__ == "__main__":
    main()