from sklearn.preprocessing import StandardScaler
import numpy as np

def PCA(X):
    # X_features:
    # each row = a feature
    # each col = an obs
    X_features = X.T

    # cov matrix: pxp
    covariance_matrix = np.cov(X_features)

    # each eigvec: px1
    # all eigvecs: pxp
    eigvals, eigvecs = np.linalg.eig(covariance_matrix)

    idx = np.argsort(eigvals)[::-1]
    eigenvalues = eigvals[idx]
    eigenvectors = eigvecs[:,idx]

    # diag matrix of eigvals pxp
    explained_variances = []
    by_total = 1 / np.sum(eigenvalues)
    for i in range(len(eigenvalues)):
        explained_variances.append(eigenvalues[i] * by_total)

    return eigenvalues, eigenvectors, explained_variances

def PCA_SVD(X):
    X_mc = X - X.mean(axis=0)
    U,S,Vt = np.linalg.svd(X_mc)

    S_sq = S**2
    idx = np.argsort(S_sq)[::-1]
    eigenvalues = S_sq[idx]
    eigenvectors = Vt.T[:,idx]

    by_total = 1/np.sum(S_sq)
    explained = [si_sq * by_total for si_sq in S_sq]

    return X_mc,explained,U,eigenvalues,eigenvectors.T
