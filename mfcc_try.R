library(ggplot2)
library(umap)

metadata_mfcc = read.csv("labels_new2.tsv", header = FALSE, sep = "\t")
metadata_mfcc = t(metadata_mfcc)
colnames(metadata_mfcc) = metadata_mfcc[1,]
row.names(metadata_mfcc) = c("num", "path", "genre", "duration")

features_mfcc = read.csv("feature_mfcc.tsv", header = FALSE, sep = "\t")
features_mfcc = t(features_mfcc)
colnames(features_mfcc) = metadata_mfcc[1,]
features_mfcc = features_mfcc[-1,]

# data cleanup
features_mfcc = features_mfcc[,colSums(is.na(features_mfcc)) == 0]
features_mfcc[!is.finite(features_mfcc)] = 0


# setting the right values together
colnames(features_mfcc) <- 1:ncol(features_mfcc)
rownames(features_mfcc) <- 1:nrow(features_mfcc)
feature_list <- list()
tmp <- c()
for (i in 1:ncol(features_mfcc)) {
  k = 1
  tmp_list <- list()
  for (j in 1:nrow(features_mfcc)) {
    if (k %% 20 == 0) {
      tmp_list[[k / 20]] <- tmp
      tmp <- features_mfcc[j, i]
    } else {
      tmp <- c(tmp, features_mfcc[j, i])
    }
    k = k+1
  }
  feature_list[[i]] <- tmp_list
}

# apply cepstral mean normalization of the mfcc features in feature_list
cmn_features <- list()
for (i in 1:length(feature_list)) {
  sample_mean <- numeric(20)  
    for (sublist in feature_list[[i]]) {
    vector <- unlist(sublist)  
    sample_mean <- sample_mean + vector
  }
  sample_mean <- sample_mean / length(feature_list[[i]])
  for (j in 1:length(feature_list[[i]])) {
    tmp_list[[j]] <- feature_list[[i]][[j]] - sample_mean
  }
  cmn_features[[i]] <- tmp_list
}


# unpack all values again
tmp_list <- list()
for (i in 1:length(cmn_features)) {
    tmp_list[[i]] <- unlist(cmn_features[[i]])
}

# create empty dataframe of length features_mfcc x features_mfcc
cmn_df <- data.frame(matrix(0, nrow = nrow(features_mfcc), ncol = ncol(features_mfcc)))
for (i in 1:length(tmp_list)) {
  cmn_df[,i] <- tmp_list[[i]]
}



library(lsa)
# loop through feature_list to calculate all cosine similarities and store them in a matrix
similarities <- matrix(0, nrow = ncol(cmn_df), ncol = ncol(cmn_df))
# for (i in 1:ncol(cmn_df)) {
  for (j in 1:ncol(cmn_df)) {
    similarities[i,j] <- dist(cmn_df[,i], cmn_df[,j], method = "euclidean")
  }
}


similarities <- dist(t(cmn_df), method = "euclidean")
similarities_matrix <- as.matrix(similarities)

n_clusters <- 20
clustering_mfcc <- hclust(similarities, method = "complete")
cluster_assignments_mfcc <- cutree(clustering_mfcc, k = n_clusters)

# do umap and colour the clusters

cluster_colors <- rainbow(n_clusters)
# assign every color in cluster_colors the value 000000
cluster_colors <- rep ("#000000", n_clusters)
cluster_colors[20] <- "#FF0000"

mfcc_umap <- umap(t(cmn_df), n_neighbors = 20, min_dist = 0.1, metric = "euclidean")
plot(mfcc_umap$layout, col = cluster_colors[cluster_assignments_mfcc], pch = n_clusters, cex = 1)
legend("bottomleft", legend = unique(cluster_assignments_mfcc), fill = cluster_colors, title = "Clusters", ncol = 2)


metadata_mfcc <- as.data.frame(metadata_mfcc)
metadata_mfcc["cluster",] <- NA
count <- 1
for (col_name in colnames(metadata_mfcc)) {
  metadata_mfcc["cluster", col_name] <- cluster_assignments_mfcc[count]
  count <- count + 1
}

colnames(similarities_matrix) <- c(1:ncol(similarities_matrix))

mean_similarities <- matrix(0, nrow = ncol(similarities_matrix), ncol = 1)
for (i in 1:ncol(similarities_matrix)) {
  mean_similarities[i,1] <- mean(similarities_matrix[,i])
}

# print the row with the lowest similarity
cat(which.min(mean_similarities), "\n")


# find some closest values
target_label <- 812
nearest_labels <- c(1:ncol(similarities_matrix))[order(similarities_matrix[target_label,])[1:20]]

cat(target_label, metadata_mfcc["path", target_label], "\n")
for (i in nearest_labels){
  cat(i, metadata_mfcc["path", i], "\n")
}

# get a list of 100 random columns in metadata_mfcc that are in cluster 16
random_list <- sample(which(metadata_mfcc["cluster",] == 6), 100)
# write those columns into a tsv file
write.table(t(metadata_mfcc[,random_list]), file = "cluster6.tsv", sep = "\t", row.names = FALSE, col.names = FALSE, quote = FALSE)
