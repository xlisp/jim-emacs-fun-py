# R data.frame vs Python pandas DataFrame Examples

### 1. Creating a DataFrame
# R:
# data <- data.frame(
#   name = c("John", "Alice", "Bob"),
#   age = c(25, 30, 35),
#   city = c("NY", "LA", "SF")
# )

# Python:
import pandas as pd

data = pd.DataFrame({
    'name': ['John', 'Alice', 'Bob'],
    'age': [25, 30, 35],
    'city': ['NY', 'LA', 'SF']
})

### 2. Selecting Columns
# R:
# # Single column
# data$name
# data[["name"]]
# 
# # Multiple columns
# data[c("name", "age")]

# Python:
# Single column
data['name']
data.name  # Only works if column name is a valid Python identifier

# Multiple columns
data[['name', 'age']]

### 3. Filtering Rows
# R:
# # Single condition
# data[data$age > 25, ]
# 
# # Multiple conditions
# data[data$age > 25 & data$city == "LA", ]

# Python:
# Single condition
data[data['age'] > 25]

# Multiple conditions
data[(data['age'] > 25) & (data['city'] == 'LA')]

### 4. Adding New Columns
# R:
# data$salary <- c(50000, 60000, 75000)
# data["salary"] <- c(50000, 60000, 75000)

# Python:
data['salary'] = [50000, 60000, 75000]
# or
data = data.assign(salary=[50000, 60000, 75000])

### 5. Grouping and Aggregation
# R:
# # Using dplyr:
# # library(dplyr)
# # data %>%
# #   group_by(city) %>%
# #   summarise(avg_age = mean(age))

# Python:
data.groupby('city')['age'].mean()
# or
data.groupby('city').agg({'age': 'mean'})

### 6. Joining/Merging DataFrames
# R:
# # df1 <- data.frame(id = c(1, 2, 3), value = c("a", "b", "c"))
# # df2 <- data.frame(id = c(1, 2, 4), score = c(90, 80, 70))
# # merge(df1, df2, by = "id", all = TRUE)  # Full outer join

# Python:
df1 = pd.DataFrame({'id': [1, 2, 3], 'value': ['a', 'b', 'c']})
df2 = pd.DataFrame({'id': [1, 2, 4], 'score': [90, 80, 70]})
pd.merge(df1, df2, on='id', how='outer')  # Full outer join

### 7. Handling Missing Values
# R:
# # Check missing values
# # is.na(data)
# # Remove rows with NA
# # na.omit(data)

# Python:
# Check missing values
data.isna()
# Remove rows with NA
data.dropna()

### 8. Basic Statistics
# R:
# # summary(data)
# # mean(data$age)
# # sd(data$age)

# Python:
data.describe()  # Summary statistics
data['age'].mean()
data['age'].std()

