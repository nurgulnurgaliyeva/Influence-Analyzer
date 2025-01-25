# InfluenceAnalyzer

## Project Overview  
**InfluenceAnalyzer** is a tool designed to identify and rank the most effective Instagram influencers within specific categories. By leveraging Natural Language Processing (NLP) and data analysis techniques, it helps uncover actionable insights such as sentiment trends, engagement patterns, and category-based influencer performance.  

If you need access to the datasets mentioned below, feel free to email me.  

---

## Repository Structure  

### **1. Codes and Extracted Data (Final Version)**  
This folder contains the final datasets and scripts used for analysis and GUI application:  

#### **Datasets**  
1. **extracted_data.csv**  
   Raw data extracted from JSON files, including user info, captions, and engagement metrics.  

2. **preprocessing_data.csv**  
   Cleaned and preprocessed data with normalized text and reordered columns.  

3. **integrate_category_and_followers.csv**  
   Merged dataset combining cleaned Instagram data with influencer categories and follower counts.  

4. **english_captions.csv**  
   Dataset filtered to include only posts with English captions and comments.  

5. **influencers_per_category.csv**  
   Summary of the number of unique influencers in each category.  

6. **cleaned_data.csv**  
   Final cleaned dataset focusing on specified categories.  

7. **sentiment_analysis.csv**  
   Results of sentiment analysis performed on the cleaned data, including sentiment scores and sentiment categories.  

8. **keywords_analysis.csv**  
   Results of keyword analysis, including top keywords and category-based classification for each post.  

9. **Number of followers for each influencer.csv**  
   Key metrics for each influencer, including username, category, follower count, following count, and total post count.  

#### **Final Code Files**  
1. **influencers_code_v3.ipynb**  
   The completed Jupyter Notebook containing the final code for the analysis, including semantic analysis.  

2. **influencers_query_gui_v2.py**  
   The final code for the GUI application that allows users to query influencer data.  

---

### **2. Original Dataset**  
This folder contains the original dataset:  
- **Dataset**  
  Includes JSON files for each Instagram post, containing structured metadata such as user information, captions, comments, likes, and other engagement metrics. The dataset spans 10,180,500 posts from 3,935 influencers across nine categories.  

---

### **3. Codes (Testing)**  
This folder contains earlier versions of the scripts, showcasing the development process:  

1. **influencers_code**  
   First version of the code where non-English captions were removed, but semantic analysis failed.  

2. **influencers_code_v2**  
   Second version of the code where merging cleaned data did not work as expected.  

3. **influencer_query_gui_v1**  
   First version of the GUI application where follower numbers were not displayed correctly.  

---

## Usage  
- **Analysis:** The Jupyter Notebook (**influencers_code_v3.ipynb**) contains the complete data processing and analysis pipeline, including sentiment and keyword analysis.  
- **GUI Application:** The Python script (**influencers_query_gui_v2.py**) provides a user-friendly interface to query influencer data based on specific metrics.  

---

## Contact  
For questions, collaborations, or access to the datasets, please email me directly.