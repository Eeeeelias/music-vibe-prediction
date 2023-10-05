library(ggplot2)
library(umap)

metadata_ld = read.csv("labels_new2.tsv", header = FALSE, sep = "\t")
metadata_ld = t(metadata_ld)
colnames(metadata_ld) = metadata_ld[1,]
row.names(metadata_ld) = c("num", "path", "genre", "duration")

features_ld = read.csv("features_low_dim.tsv", header = FALSE, sep = "\t")
features_ld = t(features_ld)
colnames(features_ld) = metadata_ld[1,]
features_ld = features_ld[-1,]

# data cleanup
features_ld = features_ld[,colSums(is.na(features_ld)) == 0]
features_ld[!is.finite(features_ld)] = 0

# clustering
n_clusters <- 20
dist_ld <- dist(t(features_ld), method = "euclidean")
clustering_ld <- hclust(dist_ld, method = "complete")
cluster_assignments_ld <- cutree(clustering_ld, k = n_clusters)

# visualize clustering using umap and color points based on cluster_assignments_ld
cluster_colors <- rainbow(n_clusters)

ld_umap <- umap(t(features_ld), n_neighbors = 20, min_dist = 0.1, metric = "euclidean")
plot(ld_umap$layout, col = cluster_colors[cluster_assignments_ld], pch = n_clusters, cex = 1)
legend("bottomright", legend = unique(cluster_assignments_ld), fill = cluster_colors, title = "Clusters", ncol = 2)

# plot an interesting subset of the data
x_min <- -5
x_max <- 5
y_min <- 10
y_max <- 20

subset_indices <- ld_umap$layout[, 1] >= x_min & ld_umap$layout[, 1] <= x_max &
  ld_umap$layout[, 2] >= y_min & ld_umap$layout[, 2] <= y_max
subset_ld_umap <- ld_umap$layout[subset_indices, ]
plot(subset_ld_umap, col = cluster_colors[cluster_assignments_ld[subset_indices]], pch = 20, cex = 1)
text(subset_ld_umap, labels = common_cols[subset_indices], pos = 3, cex = 0.7)
legend("topright", legend = unique(cluster_assignments_ld[subset_indices]), fill = cluster_colors, title = "Clusters")




metadata_ld <- as.data.frame(metadata_ld)

# fill metadata_ld with new row full of NA
metadata_ld["cluster",] <- NA
count <- 1
for (col_name in common_cols) {
  metadata_ld["cluster", col_name] <- cluster_assignments_ld[count]
  count <- count + 1
}

selected_columns <- sample(which(cluster_assignments_ld == 6), 5)
print(metadata_ld["path", selected_columns])

# This code prints a table for clusters in which the "path" column contains "NieR" 
print(table(t(metadata_ld["cluster", grepl("BigRicePiano", metadata_ld["path",])])))
print(table(t(metadata["cluster", grepl("BigRicePiano", metadata["path",])])))


# calculate overlap between metadata['cluster', ] and metadata_ld['cluster', ]
overlap <- sum(cluster_assignments_ld == cluster_assignments)
print(overlap / length(metadata['cluster', ]) * 100)

for (i in 1:length(metadata['cluster', ])) {
  tryCatch({
    if (metadata['cluster', i] != metadata_ld['cluster', i]) {
      print(i)
    }
  }, error = function(e) {} )
}


# find closet samples to 806
dist_matrix <- as.matrix(dist_ld)

target_label <- 2773

# Extract the distances for the target sample
target_distances <- dist_matrix[target_label,]

# Find the indices of the 10 samples with the smallest distances
nearest_indices <- order(target_distances)[1:10]

# Extract the labels of the 10 nearest samples
nearest_labels <- common_cols[nearest_indices]

cat(target_label, metadata_ld["path", target_label], "\n")
for (i in nearest_labels){
  cat(i, metadata_ld["path", i], "\n")
}