import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import matplotlib.lines as mlines

# Read the CSV file
df = pd.read_csv('/Users/aaronmoradi/Downloads/twitter_6m_sentiment_analyzed.csv')

# Calculate text length
df['text_length'] = df['text'].str.len()

# Handle missing values
df = df.dropna(subset=['text_length'])

# Group data for bubble size (number of texts per sentiment and text length range)
# Use 30 bins for finer granularity
df['text_length_bin'] = pd.cut(df['text_length'], bins=30)
bubble_data = df.groupby(['text_length_bin', 'sentiment_label']).agg(
    sentiment_score_avg=('sentiment_score', 'mean'),
    text_count=('text', 'count')
).reset_index()

# Prepare X-axis (bin midpoint) for text length
bubble_data['text_length_mid'] = bubble_data['text_length_bin'].apply(
    lambda x: (x.left + x.right) / 2
)

# 1. Sentiment Distribution Pie Chart
plt.figure(figsize=(8, 6))
sentiment_counts = df['sentiment_label'].value_counts()
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', 
        colors=['blue', 'red', 'black'])
plt.title('Sentiment Distribution')
plt.savefig('LiveDemoPieChartX.png')
plt.close()

# 2. Bubble Chart: Text Length vs Sentiment Score (Scaled Bubble Sizes)
plt.figure(figsize=(14, 10))  # Larger size for better readability

# Scale bubble sizes continuously based on 'text_count' (bubble sizes are proportional)
sns.scatterplot(
    x='text_length_mid',
    y='sentiment_score_avg',
    size='text_count',
    hue='sentiment_label',
    data=bubble_data,
    sizes=(50, 1000),  # Scaled range of bubble sizes
    alpha=0.6,  # Slight transparency to avoid overlap
    palette='Set1',  # Clear, distinct color palette for sentiment
    legend=False  # Remove the default legend
)

# Adjust axis limits for better spacing
plt.xlim(bubble_data['text_length_mid'].min() - 1, bubble_data['text_length_mid'].max() + 1)
plt.ylim(bubble_data['sentiment_score_avg'].min() - 0.1, bubble_data['sentiment_score_avg'].max() + 0.1)

# Adding gridlines for better visual reference
plt.grid(True, linestyle='--', alpha=0.7)

# Add titles and labels to make it clearer
plt.title('Bubble Chart: Text Length vs Sentiment Score for Different Sentiments', fontsize=16)
plt.xlabel('Average Text Length (Binned)', fontsize=12)
plt.ylabel('Average Sentiment Score', fontsize=12)

# Create custom legend with a smaller, scaled circle for smallest and largest bubble sizes
smallest_size = 50  # The minimum size defined in the 'sizes' range
largest_size = 1000  # The maximum size defined in the 'sizes' range

# Adjust the marker sizes to make sure they don't overlap
smallest_legend = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='blue', markersize=12, label=f'Min Bubble Size ({smallest_size})')
largest_legend = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='blue', markersize=20, label=f'Max Bubble Size ({largest_size})')

# Create positive and negative sentiment legend
positive_legend = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Positive Sentiment')
negative_legend = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='red', markersize=10, label='Negative Sentiment')

# Add the custom legend to the plot with smaller markers and better spacing
plt.legend(handles=[smallest_legend, largest_legend, positive_legend, negative_legend], 
           bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12, frameon=False, 
           handleheight=2, labelspacing=1.5)

# Ensure everything fits and save the figure
plt.tight_layout()
plt.savefig('LiveDemoBubbleChartX.png')
plt.close()

# Print some additional insights
print("Sentiment Analysis Summary:")
print("\nSentiment Distribution:")
print(sentiment_counts)

print("\nAverage Sentiment Scores:")
print(df.groupby('sentiment_label')['sentiment_score'].mean())
