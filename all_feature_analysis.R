library(ggplot2)

# preparing the data for analysis
metadata = read.csv("labels_new2.tsv", header = FALSE, sep = "\t")
metadata = t(metadata)
colnames(metadata) = metadata[1,]
row.names(metadata) = c("num", "path", "genre", "duration")

features = read.csv("features.tsv", header = FALSE, sep = "\t")
features = t(features)
colnames(features) = metadata[1,]
features = features[-1,]

# remove all columns that contain NA values
features = features[,colSums(is.na(features)) == 0]
# replace all infinity values with zero
features[!is.finite(features)] = 0

# apply common-scale normalization of across all columns from rows 1 to 128
features[1:128,] = scale(features[1:128,], center = TRUE, scale = TRUE)


# apply pca
pca = prcomp(t(features), center = TRUE, scale. = TRUE)

common_cols <- intersect(colnames(metadata), colnames(features))
genres <- metadata["genre", common_cols]
durations <- metadata["duration", common_cols]
durations <- as.numeric(durations)

pca_data <- data.frame(
  PC1 = pca$x[, 1],
  PC2 = pca$x[, 2],
  genre = durations,
  names = common_cols
)

# visualize 

pca_plot <- ggplot(data = pca_data, aes(x = PC1, y = PC2, color = genre)) +
  geom_point() +
  scale_color_gradient(low = "blue", high = "red") +
  # geom_text(hjust=0, vjust=0) +
  labs(x = "PC1", y = "PC2", title = "PCA Plot", color = "Duration in seconds")

print(pca_plot)

# apply clustering
kmeans = kmeans(t(features), centers = 8, iter.max = 1000, nstart = 100)
kmeans$cluster = as.factor(kmeans$cluster)

# visualize clustering with common_cols labels next to each dot
plot(features, col = kmeans$cluster, pch = 20, cex = 1)

dist <- dist(t(features), method = "euclidean")
clustering <- hclust(dist, method = "complete")
cluster_assignments <- cutree(clustering, k = 20)

# add it back to metadata

metadata <- as.data.frame(metadata)
metadata["cluster",] <- NA
count <- 1
for (col_name in common_cols) {
  metadata["cluster", col_name] <- cluster_assignments[count]
  count <- count + 1
}

# print 5 random columns of metadata that contain 8 as a cluster
print(metadata["path", sample(which(cluster_assignments == 8), 5)])

