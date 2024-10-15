import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class EDAAnalyzer:
    """
    A class used to perform exploratory data analysis (EDA) on a given DataFrame.

    Attributes:
    df (pd.DataFrame): The input DataFrame to analyze.
    target_column (str): The target variable column to focus on during analysis.
    """

    def __init__(self, df, target_column):
        """
        Initializes the EDAAnalyzer with the DataFrame and target column.

        Parameters:
        df (pd.DataFrame): The input DataFrame.
        target_column (str): The target variable to analyze.
        """
        self.df = df
        self.target_column = target_column

    def summary_statistics(self):
        """
        Generates summary statistics for numeric columns in the DataFrame.

        Returns:
        pd.DataFrame: Summary statistics for numeric columns.
        """
        return self.df.describe().T  # Transpose for better readability

    def missing_value_proportion(self):
        """
        Analyzes the proportion of missing values in each column of the DataFrame.

        Returns:
        pd.DataFrame: A DataFrame showing the proportion of missing values for
                      each column.
        """
        missing_values = self.df.isnull().sum() / len(self.df)
        missing_values_df = (
            pd.DataFrame(
                {
                    "column": missing_values.index,
                    "missing_proportion": missing_values.values,
                }
            )
            .sort_values(by="missing_proportion", ascending=False)
            .reset_index(drop=True)
        )
        return missing_values_df

    def plot_missing_data_heatmap(self):
        """
        Plots a heatmap showing missing data in the DataFrame.

        Returns:
        None: Displays a heatmap with missing data locations.
        """
        plt.figure(figsize=(12, 6))
        sns.heatmap(self.df.isnull(), cbar=False, cmap="viridis")
        plt.title("Missing Data Heatmap")
        plt.show()

    def plot_correlation_matrix(self, method="pearson"):
        """
        Plots a correlation matrix for numeric features in the DataFrame.

        Parameters:
        method (str): Method of correlation ('pearson', 'kendall', 'spearman').

        Returns:
        None: Displays a heatmap of the correlation matrix.
        """
        correlation = self.df.corr(numeric_only=True, method=method)
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Correlation Matrix")
        plt.show()

    def detect_outliers(self, column):
        """
        Detects outliers in a specific numeric column using the IQR method.

        Parameters:
        column (str): The name of the column to analyze for outliers.

        Returns:
        pd.DataFrame: A DataFrame with rows that contain outliers.
        """
        quantile_1 = self.df[column].quantile(0.25)
        quantile_3 = self.df[column].quantile(0.75)
        iqr = quantile_3 - quantile_1

        outliers = self.df[
            (self.df[column] < (quantile_1 - 1.5 * iqr))
            | (self.df[column] > (quantile_3 + 1.5 * iqr))
        ]
        return outliers

    def plot_feature_distribution(self, column, bins=30):
        """
        Plots the distribution of a specific feature, with different methods for numeric
        and categorical columns.

        Parameters:
        column (str): The name of the column for which to plot the distribution.
        bins (int): Number of bins for the histogram (numeric features only).

        Returns:
        None: Displays a plot based on the feature type (numeric or categorical).
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in the DataFrame")

        # Determine if the column is numeric or categorical
        if pd.api.types.is_numeric_dtype(self.df[column]):
            self._plot_numeric_distribution(column, bins)
        else:
            self._plot_categorical_distribution(column)

    def _plot_numeric_distribution(self, column, bins):
        """Private method to plot the distribution of a numeric column."""
        plt.figure(figsize=(8, 6))
        sns.histplot(self.df[column], bins=bins, kde=True)
        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.show()

    def _plot_categorical_distribution(self, column):
        """Private method to plot the distribution of a categorical column."""
        plt.figure(figsize=(8, 6))
        sns.countplot(x=self.df[column], order=self.df[column].value_counts().index)
        plt.title(f"Category Counts of {column}")
        plt.xlabel(column)
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")  # Rotate labels
        plt.show()

    def plot_boxplot(self, column, by=None):
        """
        Plots a boxplot of a numeric column,
        optionally grouped by a categorical feature.

        Parameters:
        column (str): Numeric column to plot.
        by (str or None): Categorical column to group by.
        If None, no grouping is applied.

        Returns:
        None: Displays a box plot.
        """
        plt.figure(figsize=(8, 6))

        if by:
            sns.boxplot(x=self.df[by], y=self.df[column])
            plt.title(f"Boxplot of {column} by {by}")
            plt.xlabel(by)
            plt.ylabel(column)
        else:
            sns.boxplot(x=self.df[column])
            plt.title(f"Boxplot of {column}")

        plt.show()

    def plot_pairplot(self, hue=None):
        """
        Plots a pair plot for numeric features in the DataFrame.

        Parameters:
        hue (str): Optional. Column to use for color encoding (typically a categorical
                   variable).

        Returns:
        None: Displays a pair plot.
        """
        sns.pairplot(self.df, hue=hue)
        plt.title("Pair Plot")
        plt.show()

    def plot_target_distribution(self, bins=30, kde=True):
        """
        Plots the distribution of the target variable, automatically determining whether
        it's numeric, binary, or categorical. Customization options are available for
        bins and KDE.

        Parameters:
        bins (int): Number of bins to use for the histogram (numeric targets only).
                    Default is 30.
        kde (bool): Whether to add KDE to the numeric target distribution plot.
                    Default is True.

        Returns:
        None: Displays a plot of the target distribution.
        """
        unique_values = self.df[self.target_column].nunique()

        # Handle Binary Target (even if it's numeric)
        if unique_values == 2:
            print(f"Detected binary target: {self.target_column}")
            plt.figure(figsize=(8, 6))
            sns.countplot(
                x=self.df[self.target_column],
                order=self.df[self.target_column].value_counts().index,
            )

            # Add percentage annotations
            total = len(self.df[self.target_column])
            for p in plt.gca().patches:
                percentage = f"{100 * p.get_height() / total:.1f}%"
                plt.gca().annotate(
                    percentage,
                    (p.get_x() + p.get_width() / 2.0, p.get_height()),
                    ha="center",
                    va="baseline",
                )

            plt.title(f"Distribution of Binary Target: {self.target_column}")
            plt.xlabel(self.target_column)
            plt.ylabel("Count")
            plt.show()

        # Numeric Target
        elif (
            pd.api.types.is_numeric_dtype(self.df[self.target_column])
            and unique_values > 2
        ):
            print(f"Detected numeric target: {self.target_column}")
            plt.figure(figsize=(8, 6))
            sns.histplot(self.df[self.target_column], bins=bins, kde=kde)
            plt.title(f"Distribution of Numeric Target: {self.target_column}")
            plt.xlabel(self.target_column)
            plt.ylabel("Frequency")
            plt.show()

        # Categorical Target
        else:
            print(f"Detected categorical target: {self.target_column}")
            plt.figure(figsize=(8, 6))
            sns.countplot(
                x=self.df[self.target_column],
                order=self.df[self.target_column].value_counts().index,
            )

            # Add percentage annotations
            total = len(self.df[self.target_column])
            for p in plt.gca().patches:
                percentage = f"{100 * p.get_height() / total:.1f}%"
                plt.gca().annotate(
                    percentage,
                    (p.get_x() + p.get_width() / 2.0, p.get_height()),
                    ha="center",
                    va="baseline",
                )

            plt.title(f"Distribution of Categorical Target: {self.target_column}")
            plt.xlabel(self.target_column)
            plt.ylabel("Count")
            plt.xticks(rotation=45, ha="right")  # Rotate labels for readability
            plt.show()

    def value_counts(self, column, round_by=2):
        """
        Returns a DataFrame with the value counts and percentage distribution of a
        categorical column.

        Parameters:
        column (str): The name of the categorical column to analyze.
        round_by (int): Number of decimal places to round the percentage values.
                        Default is 2.

        Returns:
        pd.DataFrame: A DataFrame with two columns:
                      - column_name_num: Absolute count of each category.
                      - column_name_pct: Percentage distribution of each category,
                        rounded to the specified number of decimal places.
        """
        column_dist_num = pd.DataFrame(self.df[column].value_counts(normalize=False))
        column_dist_pct = pd.DataFrame(
            self.df[column].value_counts(normalize=True).round(round_by)
        )
        column_dist_df = column_dist_num.merge(
            column_dist_pct,
            left_index=True,
            right_index=True,
            suffixes=["_num", "_pct"],
        ).reset_index()
        return column_dist_df

    def analyze_all_features(self):
        """
        Automatically analyzes all features in the DataFrame by applying appropriate
        methods for numeric and categorical columns.

        Returns:
        None: Displays the analysis results for each feature.
        """
        for column in self.df.columns:
            print(f"\nAnalyzing Feature: {column}")
            print("=" * 50)

            if pd.api.types.is_numeric_dtype(self.df[column]):
                print(f"Summary Statistics for Numeric Feature: {column}")
                print(self.df[column].describe())

                print(f"\nPlotting Distribution for {column}...")
                self.plot_feature_distribution(column)

                print(f"\nDetecting Outliers in {column}...")
                outliers = self.detect_outliers(column)
                print(f"Found {len(outliers)} outliers in {column}.")

            else:
                print(f"Value Counts for Categorical Feature: {column}")
                print(self.df[column].value_counts())

                print(f"\nPlotting Distribution for {column}...")
                self.plot_feature_distribution(column)

    def run_global_eda(self):
        """
        Runs broader exploratory data analysis steps such as correlation matrix, missing
        data heatmap, pair plot, and target distribution analysis.

        Returns:
        None: Displays the results of the global EDA analysis.
        """
        print("\nAnalyzing Info...")
        print(self.df.info())

        print("\nAnalyzing Summary Statistics...")
        print(self.summary_statistics())

        print("\nRunning Missing Data Proportion...")
        print(self.missing_value_proportion())

        print("\nRunning Missing Data Heatmap...")
        self.plot_missing_data_heatmap()

        print("\nAnalyzing Target Distribution...")
        self.plot_target_distribution()

        print("\nRunning Correlation Matrix Analysis...")
        self.plot_correlation_matrix()

        print("\nGenerating Pair Plot for Numeric Features...")
        self.plot_pairplot()
