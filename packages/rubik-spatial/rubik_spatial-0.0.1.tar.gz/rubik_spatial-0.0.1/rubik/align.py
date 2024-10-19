import numpy as np
from skimage.transform import AffineTransform, EuclideanTransform, warp 
from skimage.feature import ORB, match_descriptors
from skimage.measure import ransac
import scanpy as sc
import squidpy as sq
import Pseudovisium.pseudovisium_generate as pvg
import matplotlib.pyplot as plt


def find_affine_transform_single_channel(channel1, channel2, max_features=3000, affine_or_euclidean='affine'):
    """
    Find the affine or Euclidean transform between two single-channel images.

    Args:
        channel1 (np.ndarray): First input channel.
        channel2 (np.ndarray): Second input channel.
        max_features (int): Maximum number of features to detect.
        affine_or_euclidean (str): Type of transform to use ('affine' or 'euclidean').

    Returns:
        skimage.transform.AffineTransform: Estimated transform model.
    """
    channel1 = channel1.squeeze()
    channel2 = channel2.squeeze()
    
    orb = ORB(n_keypoints=max_features, fast_threshold=0.05)
    
    orb.detect_and_extract(channel1)
    keypoints1, descriptors1 = orb.keypoints, orb.descriptors
    orb.detect_and_extract(channel2)
    keypoints2, descriptors2 = orb.keypoints, orb.descriptors

    matches = match_descriptors(descriptors1, descriptors2, cross_check=True)

    src = keypoints2[matches[:, 1]][:, ::-1]
    dst = keypoints1[matches[:, 0]][:, ::-1]
    transform = AffineTransform if affine_or_euclidean == 'affine' else EuclideanTransform
    model, inliers = ransac((src, dst), 
                            transform,
                            min_samples=3,
                            residual_threshold=3, 
                            max_trials=20000)

    return model if model else AffineTransform()

def find_affine_transform_multi_channel(original, transformed, affine_or_euclidean='affine'):
    """
    Find the affine or Euclidean transform between two multi-channel images.

    Args:
        original (np.ndarray): Original multi-channel image.
        transformed (np.ndarray): Transformed multi-channel image.
        affine_or_euclidean (str): Type of transform to use ('affine' or 'euclidean').

    Returns:
        skimage.transform.AffineTransform: Estimated transform model.
    """
    if original.ndim == 2 or original.shape[2] == 1:
        return find_affine_transform_single_channel(original, transformed)
    
    transforms = []
    for channel in range(original.shape[2]):
        model = find_affine_transform_single_channel(
            original[:,:,channel],
            transformed[:,:,channel],
            affine_or_euclidean=affine_or_euclidean
        )
        transforms.append(model)
    
    combined_matrix = np.mean([t.params for t in transforms], axis=0)
    return AffineTransform(matrix=combined_matrix)


def pad_images(image1, image2):
    """
    Pad two images to the same size.

    Args:
        image1 (np.ndarray): First image.
        image2 (np.ndarray): Second image.

    Returns:
        tuple: Padded versions of image1 and image2.
    """
    max_height = max(image1.shape[0], image2.shape[0])
    max_width = max(image1.shape[1], image2.shape[1])
    
    pad_image1 = np.zeros((max_height, max_width, image1.shape[2]), dtype=image1.dtype)
    pad_image2 = np.zeros((max_height, max_width, image2.shape[2]), dtype=image2.dtype)
    
    pad_image1[:image1.shape[0], :image1.shape[1], :] = image1
    pad_image2[:image2.shape[0], :image2.shape[1], :] = image2
    
    return pad_image1, pad_image2

def calculate_weighted_mse(image1, image2, weight=1.0):
    """
    Calculate the weighted mean squared error between two images.

    Args:
        image1 (np.ndarray): First image.
        image2 (np.ndarray): Second image.
        weight (float): Weight for the error calculation.

    Returns:
        np.ndarray: Array of weighted MSE values for each channel.
    """
    padded_image1, padded_image2 = pad_images(image1, image2)
    mse = np.mean((padded_image1 - padded_image2) ** 2, axis=(0, 1))
    return mse * weight

def align_images(original, transformed, affine_or_euclidean='affine'):
    """
    Align two images using affine or Euclidean transform.

    Args:
        original (np.ndarray): Original image.
        transformed (np.ndarray): Image to be aligned.
        affine_or_euclidean (str): Type of transform to use ('affine' or 'euclidean').

    Returns:
        tuple: Aligned image and the estimated transform.
    """
    padded_original, padded_transformed = pad_images(original, transformed)
    
    # Find the affine transform
    affine_transform = find_affine_transform_multi_channel(padded_original, padded_transformed, affine_or_euclidean=affine_or_euclidean)
    
    # Apply the affine transform
    aligned_image = warp(padded_transformed, affine_transform.inverse, output_shape=padded_original.shape)
    
    # Crop the aligned image to the original size
    aligned_image = aligned_image[:original.shape[0], :original.shape[1], :]
    
    return aligned_image, affine_transform

def get_target_genes(adata, n_genes=10):
    """
    Process AnnData object and return top spatially autocorrelated genes.

    Args:
        adata (anndata.AnnData): Input AnnData object.
        n_genes (int): Number of top genes to return.

    Returns:
        pandas.Index: Index of top spatially autocorrelated genes.
    """
    sc.pp.filter_genes(adata, min_cells=10)
    sc.pp.filter_cells(adata, min_genes=50)
    sc.pp.filter_cells(adata, min_counts=50)
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sq.gr.spatial_neighbors(adata, radius=150, coord_type="generic")
    sq.gr.spatial_autocorr(
        adata,
        mode="moran",
        n_perms=100,
        n_jobs=1,
    )
    res = adata.uns["moranI"].head(n_genes)
    return res.index

def create_gene_images(adata, genes=None, res=1, further_binning = True):
    """
    Create image representations of gene expression for specified genes.

    Args:
        adata (anndata.AnnData): Input AnnData object.
        genes (list): List of gene names to process.
        res (int): Resolution for spatial binning.

    Returns:
        np.ndarray: Array of gene expression images.
    """
    
    if further_binning:
        if genes is None:
            raise ValueError("Genes must be specified for further binning.")
        
        sc.pp.filter_genes(adata, min_cells=100)
        sc.pp.filter_cells(adata, min_genes=30)
        sc.pp.filter_cells(adata, min_counts=40)
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)

        adata_subset = sc.AnnData(adata.X[:,adata.var.index.isin(genes)], obs=adata.obs, var=adata.var[adata.var.index.isin(genes)])
        adata_subset.obsm = adata.obsm
        adata_subset.uns = adata.uns
        adata_raster = pvg.spatial_binning_adata(adata_subset, res, "square")
    else:
        adata_raster = adata.copy()
    
    
    gene_image_list = []
    for gene in genes:
        max_x = adata_raster.obsm["spatial"][:,0].max() // res
        max_y = adata_raster.obsm["spatial"][:,1].max() // res
        gene_image = np.zeros((int(max_x)+1, int(max_y)+1))
        
        for x, y, i in zip(adata_raster.obsm["spatial"][:,0], adata_raster.obsm["spatial"][:,1], range(adata_raster.n_obs)):
            value = adata_raster.X[i, adata_raster.var.index==gene].toarray()[0]
            gene_image[int(x//res), int(y//res)] += value[0]
        
        gene_image = (gene_image - gene_image.min()) / (gene_image.max() - gene_image.min()) * 255
        gene_image_list.append(gene_image)
    
    gene_image_array = np.array(gene_image_list)
    gene_image_array = np.moveaxis(gene_image_array, 0, -1)
    return gene_image_array


def plot_mse_histograms(mse_before_list, mse_after_list, titles):
    """
    Plot histograms of mean squared errors before and after alignment for each pair of images.

    Args:
        mse_before_list (list): List of MSE arrays before alignment.
        mse_after_list (list): List of MSE arrays after alignment.
        titles (list): List of titles for each histogram pair.
    """
    n_alignments = len(mse_before_list)
    fig, axs = plt.subplots(n_alignments, 2, figsize=(20, 5 * n_alignments), squeeze=False)
    
    for i, (mse_before, mse_after, title) in enumerate(zip(mse_before_list, mse_after_list, titles)):
        axs[i, 0].hist(mse_before, bins=20, alpha=0.5, label='Before')
        axs[i, 0].hist(mse_after, bins=20, alpha=0.5, label='After')
        axs[i, 0].set_title(f'{title} - Histogram')
        axs[i, 0].set_xlabel('Mean Squared Error')
        axs[i, 0].set_ylabel('Frequency')
        axs[i, 0].legend()

        axs[i, 1].scatter(mse_before, mse_after)
        axs[i, 1].set_title(f'{title} - Scatter')
        axs[i, 1].set_xlabel('MSE Before Alignment')
        axs[i, 1].set_ylabel('MSE After Alignment')
        axs[i, 1].plot([0, max(mse_before.max(), mse_after.max())], 
                       [0, max(mse_before.max(), mse_after.max())], 
                       'r--', label='y=x')
        axs[i, 1].legend()
    
    plt.tight_layout()
    plt.show()

def process_and_align_spatial_data(adata_list, n_genes=5, resolution=50, affine_or_euclidean='affine', correction=False):
    """
    Process multiple spatial transcriptomics datasets, identify top genes, create gene expression images, and align them.

    Args:
        adata_list (list): List of AnnData objects with full resolution data.
        n_genes (int): Number of top genes to process.
        resolution (int): Resolution for spatial binning.
        affine_or_euclidean (str): Type of transform to use for alignment ('affine' or 'euclidean').
        correction (bool): Whether to apply weighted correction for alignments.

    Returns:
        tuple: List of aligned gene images, list of original gene images, list of estimated transforms, 
               list of MSE scores before alignment, and list of MSE scores after alignment.
    """
    if len(adata_list) < 2:
        raise ValueError("At least two AnnData objects are required for alignment.")

    # Create hexagonal binned data for all datasets
    adata_hex_list = [pvg.spatial_binning_adata(adata, 50, "hex") for adata in adata_list]

    # Get target genes from all datasets
    target_genes = []
    for adata in adata_hex_list:
        target_genes.append(get_target_genes(adata, n_genes=n_genes))
    target_genes = list(set([gene for genes in target_genes for gene in genes]))
    
    # Create gene images for all datasets
    gene_images = [create_gene_images(adata, target_genes, resolution) for adata in adata_list]

    aligned_images = [gene_images[0]]  # First image is the reference
    transforms = [AffineTransform()]  # Identity transform for the first image
    mse_before_scores = []
    mse_after_scores = []

    for i in range(1, len(gene_images)):
        if correction:
            # Align with all other images and compute weighted average
            weighted_transform = AffineTransform()
            total_weight = 0
            mse_before_sum = np.zeros(gene_images[i].shape[2])
            mse_after_sum = np.zeros(gene_images[i].shape[2])

            for j in range(len(gene_images)):
                if i == j:
                    continue
                weight = 1 - abs(i - j) / len(gene_images)
                mse_before = calculate_weighted_mse(gene_images[i], gene_images[j], weight)
                mse_before_sum += mse_before

                aligned_image, transform = align_images(gene_images[j], gene_images[i], affine_or_euclidean)
                weighted_transform.params += transform.params * weight
                total_weight += weight
                
                mse_after = calculate_weighted_mse(aligned_image, gene_images[j], weight)
                mse_after_sum += mse_after
            
            weighted_transform.params /= total_weight
            aligned_image = warp(gene_images[i], weighted_transform.inverse, output_shape=gene_images[0].shape)
            transforms.append(weighted_transform)
            mse_before_scores.append(mse_before_sum / total_weight)
            mse_after_scores.append(mse_after_sum / total_weight)
        else:
            # Align only with the previous image
            mse_before = calculate_weighted_mse(gene_images[i], gene_images[i-1])
            aligned_image, transform = align_images(gene_images[i-1], gene_images[i], affine_or_euclidean)
            transforms.append(transform)
            mse_after = calculate_weighted_mse(aligned_image, gene_images[i-1])
            mse_before_scores.append(mse_before)
            mse_after_scores.append(mse_after)

        aligned_images.append(aligned_image)

    # Plot MSE histograms
    titles = [f'Alignment {i+1} to {i}' for i in range(1, len(gene_images))]
    plot_mse_histograms(mse_before_scores, mse_after_scores, titles)

    return aligned_images, gene_images, transforms, mse_before_scores, mse_after_scores




def raw_workflow_process_and_align_spatial_data(adata_list, n_genes=5, resolution=50, affine_or_euclidean='affine', correction=False, further_binning=False):
    """
    Process multiple spatial transcriptomics datasets, identify top genes, create gene expression images, and align them.

    Args:
        adata_list (list): List of AnnData objects with full resolution data.
        n_genes (int): Number of top genes to process.
        resolution (int): Resolution for spatial binning.
        affine_or_euclidean (str): Type of transform to use for alignment ('affine' or 'euclidean').
        correction (bool): Whether to apply weighted correction for alignments.

    Returns:
        tuple: List of aligned gene images, list of original gene images, list of estimated transforms, 
               list of MSE scores before alignment, and list of MSE scores after alignment.
    """
    if len(adata_list) < 2:
        raise ValueError("At least two AnnData objects are required for alignment.")

    # Create gene images for all datasets
    gene_images = [create_gene_images(adata, None, resolution,further_binning) for adata in adata_list]

    aligned_images = [gene_images[0]]  # First image is the reference
    transforms = [AffineTransform()]  # Identity transform for the first image
    mse_before_scores = []
    mse_after_scores = []

    for i in range(1, len(gene_images)):
        if correction:
            # Align with all other images and compute weighted average
            weighted_transform = AffineTransform()
            total_weight = 0
            mse_before_sum = np.zeros(gene_images[i].shape[2])
            mse_after_sum = np.zeros(gene_images[i].shape[2])

            for j in range(len(gene_images)):
                if i == j:
                    continue
                weight = 1 - abs(i - j) / len(gene_images)
                mse_before = calculate_weighted_mse(gene_images[i], gene_images[j], weight)
                mse_before_sum += mse_before

                aligned_image, transform = align_images(gene_images[j], gene_images[i], affine_or_euclidean)
                weighted_transform.params += transform.params * weight
                total_weight += weight
                
                mse_after = calculate_weighted_mse(aligned_image, gene_images[j], weight)
                mse_after_sum += mse_after
            
            weighted_transform.params /= total_weight
            aligned_image = warp(gene_images[i], weighted_transform.inverse, output_shape=gene_images[0].shape)
            transforms.append(weighted_transform)
            mse_before_scores.append(mse_before_sum / total_weight)
            mse_after_scores.append(mse_after_sum / total_weight)
        else:
            # Align only with the previous image
            mse_before = calculate_weighted_mse(gene_images[i], gene_images[i-1])
            aligned_image, transform = align_images(gene_images[i-1], gene_images[i], affine_or_euclidean)
            transforms.append(transform)
            mse_after = calculate_weighted_mse(aligned_image, gene_images[i-1])
            mse_before_scores.append(mse_before)
            mse_after_scores.append(mse_after)

        aligned_images.append(aligned_image)

    # Plot MSE histograms
    titles = [f'Alignment {i+1} to {i}' for i in range(1, len(gene_images))]
    plot_mse_histograms(mse_before_scores, mse_after_scores, titles)

    return aligned_images, gene_images, transforms, mse_before_scores, mse_after_scores
