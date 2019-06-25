from sklearn.cluster import KMeans
from pyclustering.cluster.xmeans import xmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster import cluster_visualizer

# https://codedocs.xyz/annoviko/pyclustering/classpyclustering_1_1cluster_1_1xmeans_1_1xmeans.html#details -> XMeans
#https://codedocs.xyz/annoviko/pyclustering/xmeans_8py_source.html -> XMeans

# sklearn.cluster.KMeans(
# 	n_clusters=8, 					-> numarul de clustere folosit pentru a selecta centroizii 
# 	init=’k-means++’,  				-> ‘k-means++’ selects initial cluster centers for k-mean clustering in a smart way to speed up convergence. 
# 									   ‘random’: choose k observations (rows) at random from data for the initial centroids.		
# 									   ‘ndarray’ it should be of shape (n_clusters, n_features) and gives the initial centers.
# 	n_init=10, 						-> numarul de ori de care va fi rulat algoritmul
# 	max_iter=300, 					-> numarul de iteratii maxim pentru o rulare a algoritmului
# 	tol=0.0001, 					-> toleranta
# 	precompute_distances=’auto’,    -> ‘auto’: do not precompute distances if n_samples * n_clusters > 12 million. 
# 									   ‘True’: always precompute distances
# 									   ‘False’: never precompute distances
# 	verbose=0, 						-> verbose mode		
# 	random_state=None, 				-> determina determinismul modaltatii random de gasire a centroizilor initiali
# 	copy_x=True, 					-> 
# 	n_jobs=None, 					-> nr de threaduri
# 	algorithm=’auto’)				-> K-means algorithm to use in functie de sparsitatea datelor. 

# pyclustering.cluster.xmeans.xmeans(	 	
# 	data, 														-> lista de puncte
# 	initial_centers = None, 									-> coordonatele centrelor initiale
# 	kmax = 20, 													-> numarul maxim de clustere
# 	tolerance = 0.025, 											-> daca valoarea maxima de schimbare a centrelor clusterelor este mai mica decat asta, algoritmul se opreste
# 	criterion = splitting_type.BAYESIAN_INFORMATION_CRITERION,  -> tipul criteriei de splitare
# 	ccore = True              									-> C++ pyclustering library
# )		


###
### Aplica kmeans.
### param X: vectorii pe care se aplica algoritmul.
### param n_clusters: numarul de clustere.
### param max_iter: numarul de iteratii pe care se ruleaza algoritul.
### param n_jobs: numarul de threaduri.
### param random_state: determina determinismul modaltatii random de gasire a centroizilor initiali.
### return kmeans: rezultatul clusterizarii, obiect sklearn.cluster.KMeans.
###
def apply_KMeans(X, n_clusters, max_iter=300, n_init=10, n_jobs=8, random_state=10 ):
	kmeans = KMeans(n_clusters = n_clusters, init = 'k-means++', max_iter = max_iter, n_init = n_init, random_state = random_state)
	kmeans.fit(X)
	return kmeans

###
### Aplica XMeans. X-Means clustering algorithm, an extended K-Means which tries to automatically determine the number of clusters based on BIC scores. Starting with only one cluster, the X-Means algorithm goes into action after each run of K-Means, making local decisions about which subset of the current centroids should split themselves in order to better fit the data. The splitting decision is done by computing the Bayesian Information Criterion (BIC)
### param X: lista de liste cu puncte.
### param nr_cluster_initial: numarul de la clustere de la care se pleaca.
### param kmax: numarul maxim de clustere la care se poate ajunge
### return xmeans_instance: obiect pyclustering.cluster.xmeans.xmeans
###
def apply_XMeans(X, nr_cluster_initial, kmax):
	initial_centers = kmeans_plusplus_initializer(X, nr_cluster_initial).initialize()

	xmeans_instance = xmeans(X, initial_centers, kmax)
	xmeans_instance.process()

	return xmeans_instance


