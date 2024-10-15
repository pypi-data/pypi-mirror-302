# collaborative_recommender.py

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors


class CollaborativeRecommender:
    def __init__(self, user_item_matrix: pd.DataFrame, tools_df: pd.DataFrame, n_neighbors: int = 5):
        # Check if user_item_matrix is empty
        if user_item_matrix.empty:
            raise ValueError(
                "User-item matrix is empty. Cannot proceed with collaborative filtering.")

        self.user_item_matrix = user_item_matrix.astype(float)
        self.tools_df = tools_df

        # Adjust n_neighbors to ensure it's within a valid range.
        self.n_neighbors = min(n_neighbors, len(user_item_matrix))

        tool_ids_in_matrix = set(user_item_matrix.columns)
        tool_ids_in_tools_df = set(tools_df['tool_id'])
        missing_tool_ids = tool_ids_in_matrix - tool_ids_in_tools_df
        if missing_tool_ids:
            raise ValueError(
                f"User-item matrix contains tool_ids not present in tools_df: {missing_tool_ids}")

        if tools_df['tool_id'].duplicated().any():
            raise ValueError("Duplicate tool_ids found in tools_df.")

        if self.n_neighbors < 1:
            raise ValueError("n_neighbors must be at least 1.")

        self.model = NearestNeighbors(
            metric='cosine', algorithm='brute', n_neighbors=self.n_neighbors)
        self.model.fit(self.user_item_matrix)

        self.tool_id_to_details = self.tools_df.set_index(
            'tool_id').to_dict('index')
        self.all_tool_ids = set(self.tools_df['tool_id'].unique())

    def get_recommendation_scores(self, user_id: int) -> pd.Series:
        if user_id not in self.user_item_matrix.index:
            raise ValueError(
                f"User ID {user_id} not found in the user-item matrix.")

        user_vector = self.user_item_matrix.loc[user_id].values.reshape(1, -1)

        if np.all(user_vector == 0.0):
            return self.user_item_matrix.mean()

        n_neighbors = min(self.n_neighbors, len(self.user_item_matrix))
        distances, indices = self.model.kneighbors(
            user_vector, n_neighbors=n_neighbors)

        similar_users_indices = indices.flatten()
        similar_users_ratings = self.user_item_matrix.iloc[similar_users_indices]
        mean_ratings = similar_users_ratings.mean(axis=0)

        return mean_ratings

    def get_recommendations(self, user_id: int, n_recommendations: int = 5) -> list:
        if n_recommendations < 1:
            raise ValueError("n_recommendations must be at least 1.")

        if user_id not in self.user_item_matrix.index:
            raise ValueError(
                f"User ID {user_id} not found in the user-item matrix.")

        user_vector = self.user_item_matrix.loc[user_id].values.reshape(1, -1)

        if np.all(user_vector == 0.0):
            tool_ratings = self.user_item_matrix.mean().sort_values(ascending=False)
            top_recommendations = tool_ratings.head(n_recommendations)
            recommended_tools = self.tools_df[self.tools_df['tool_id'].isin(
                top_recommendations.index)]
            return recommended_tools.to_dict('records')

        n_neighbors = min(self.n_neighbors, len(self.user_item_matrix))
        distances, indices = self.model.kneighbors(
            user_vector, n_neighbors=n_neighbors)

        similar_users_indices = indices.flatten()
        similar_users_ratings = self.user_item_matrix.iloc[similar_users_indices]
        mean_ratings = similar_users_ratings.mean(axis=0)

        user_rated_tools = set(
            self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index)
        potential_recommendations = mean_ratings.drop(
            labels=user_rated_tools, errors='ignore')
        sorted_recommendations = potential_recommendations.sort_values(
            ascending=False)

        top_tool_ids = sorted_recommendations.head(
            n_recommendations).index.tolist()
        recommended_tools = []

        for tool_id in top_tool_ids:
            if tool_id in self.tool_id_to_details:
                tool_details = self.tool_id_to_details[tool_id]
                recommended_tool = {
                    'tool_id': tool_id,
                    'tool_name': tool_details.get('name', ''),
                    'category': tool_details.get('category', ''),
                    'features': tool_details.get('features', ''),
                    'cost': tool_details.get('cost', ''),
                    'description': tool_details.get('description', ''),
                    'url': tool_details.get('url', ''),
                    'language': tool_details.get('language', ''),
                    'platform': tool_details.get('platform', '')
                }
                recommended_tools.append(recommended_tool)

        return recommended_tools

    def __repr__(self):
        return (f"CollaborativeRecommender(n_neighbors={self.n_neighbors}, "
                f"number_of_tools={len(self.all_tool_ids)})")
