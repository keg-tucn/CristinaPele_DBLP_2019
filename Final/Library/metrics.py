import matplotlib.pyplot as plt # vizualizari

from sklearn.metrics import silhouette_score
import matplotlib.cm as cm


# gensim.models.word2vec.Word2Vec.score(
#   sentences,                  -> lista de liste (propozitii)
#   total_sentences=1000000,    -> numarul de propozitii
#   chunksize=100,              -> chunksize de joburi
#   queue_factor=2,             -> multiplu de cozi
#   report_delay=1)             -> secunde de asteptat pana la raport

###
### Aplica KMeans si elbow method pe vectorii documentelor.
### param X: vectorii.
### param range: numarul maxim de clustere.
### return wcss
###
def elbow_kmeans(X, range):
    wcss = []
    for i in range(1,range):
        if i % 10 == 0:
            print (i)
        kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 500, n_init = 10, random_state = 0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_) 

        plt.plot(range(1,range), wcss, 'r')
        plt.title('The elbow method')
        plt.xlabel('The number of clusters')
        plt.ylabel('WCSS')
        plt.show()

    return wcss


###
### Aplica silhouette.
### param X: lista de vectori
### param cluster_labels: lista de labels pentru vectori
###
def apply_silhouette(X, cluster_labels):
    silhouette_avg = silhouette_score(X, cluster_labels)
    print("The average silhouette_score is :", silhouette_avg) 


