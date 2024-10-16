class printer:
    def __init__(self):
        self.a = 1

    def clustering(self):
        print('''
       import pandas as pd
        import numpy as np
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import KMeans
        from sklearn.decomposition import PCA
        import matplotlib.pyplot as plt
        from nltk.corpus import stopwords
        import string

        def preprocess_text(text):
            # Convert text to lowercase
            text = text.lower()
            # Remove punctuation
            text = text.translate(str.maketrans('', '', string.punctuation))
            # Remove stopwords
            return text

        documents = [
            "Data Science is a field that uses scientific methods to extract knowledge from data.",
            "Machine Learning is a subset of Artificial Intelligence that involves training models on data.",
            "Deep learning techniques such as neural networks have achieved great success in recent years.",
            "Natural Language Processing (NLP) is the field focused on making sense of human language.",
            "Reinforcement Learning is used in various applications including robotics and games.",
            "The rise of big data has led to a surge in demand for data scientists.",
            "Supervised learning is the task of learning a function that maps an input to an output based on example input-output pairs.",
            "Unsupervised learning finds hidden patterns or intrinsic structures in input data.",
            "Clustering is a type of unsupervised learning where data points are grouped based on similarity.",
        ]

        # Preprocess documents
        documents = [preprocess_text(doc) for doc in documents]

        # Convert the text data into TF-IDF feature vectors
        tfidf_vectorizer = TfidfVectorizer(max_df=0.8, min_df=2, stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

        print("TF-IDF matrix shape:", tfidf_matrix.shape)

        # Set the number of clusters (k)
        num_clusters = 3

        # Fit the KMeans model
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(tfidf_matrix)

        # Get the cluster labels for each document
        cluster_labels = kmeans.labels_

        # Print the cluster labels for each document
        for i, doc in enumerate(documents):
            print(f"Document {i+1}: Cluster {cluster_labels[i]}")


        # Reduce dimensions using PCA for 2D visualization
        pca = PCA(n_components=2, random_state=42)
        tfidf_matrix_2d = pca.fit_transform(tfidf_matrix.toarray())

        # Plot the clustered documents
        plt.figure(figsize=(10, 6))
        plt.scatter(tfidf_matrix_2d[:, 0], tfidf_matrix_2d[:, 1], c=cluster_labels, cmap='viridis', s=100)
        plt.title('Document Clustering')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.colorbar()
        plt.show()

        def print_top_terms_per_cluster(tfidf_vectorizer, kmeans, num_terms=5):
            order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
            terms = tfidf_vectorizer.get_feature_names_out()

            for i in range(num_clusters):
                print(f"\nCluster {i} top terms:")
                for ind in order_centroids[i, :num_terms]:
                    print(terms[ind])

        # Print top terms per cluster
        print_top_terms_per_cluster(tfidf_vectorizer, kmeans)

       ''')

    def recommender(self):
        print('''
            import numpy as np
            import pandas as pd

            # Sample user-item matrix (rows: users, columns: items)
            data = {
                'Item1': [5, 3, 0, 1],
                'Item2': [4, 0, 0, 1],
                'Item3': [1, 1, 0, 5],
                'Item4': [1, 0, 0, 4],
                'Item5': [0, 1, 5, 4],
            }

            user_item_matrix = pd.DataFrame(data, index=['User1', 'User2', 'User3', 'User4'])
            print("User-Item Matrix:")
            print(user_item_matrix)
            from sklearn.metrics.pairwise import cosine_similarity

            # User-User Similarity Matrix (rows: users, columns: users)
            user_similarity = cosine_similarity(user_item_matrix)
            user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

            # Item-Item Similarity Matrix (rows: items, columns: items)
            item_similarity = cosine_similarity(user_item_matrix.T)
            item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

            print("\nUser-User Similarity Matrix:")
            print(user_similarity_df)

            print("\nItem-Item Similarity Matrix:")
            print(item_similarity_df)

            def recommend_items_user(user_id, user_item_matrix, item_similarity, top_n=3):
                user_ratings = user_item_matrix.loc[user_id]

                # Calculate weighted average item scores based on item-item similarity
                item_scores = user_item_matrix.dot(item_similarity)
                user_item_scores = item_scores.loc[user_id]

                # Recommend top N items the user has not interacted with
                already_rated = user_ratings[user_ratings > 0].index
                recommendations = user_item_scores.drop(already_rated).sort_values(ascending=False).head(top_n)

                return recommendations

            # Example: Recommend items for 'User1' based on item-item similarity
            recommendations = recommend_items_user('User1', user_item_matrix, item_similarity_df)
            print("\nTop Recommendations for User1 (Item-Item Based):")
            print(recommendations)

            def recommend_items_user_based(user_id, user_item_matrix, user_similarity, top_n=3):
                user_index = user_item_matrix.index.get_loc(user_id)

                # Get similar users to the target user
                similar_users = user_similarity[user_index]

                # Calculate weighted average item scores based on user similarity
                weighted_item_scores = similar_users.dot(user_item_matrix) / np.array([np.abs(similar_users).sum()])

                # Get the user's ratings and sort the items that haven't been rated by the user
                user_ratings = user_item_matrix.loc[user_id]
                already_rated = user_ratings[user_ratings > 0].index
                recommendations = pd.Series(weighted_item_scores, index=user_item_matrix.columns).drop(already_rated)

                return recommendations.sort_values(ascending=False).head(top_n)

            # Example: Recommend items for 'User1' based on user-user similarity
            user_based_recommendations = recommend_items_user_based('User2', user_item_matrix, user_similarity)
            print("\nTop Recommendations for User1 (User-User Based):")
            print(user_based_recommendations)
            ''')

