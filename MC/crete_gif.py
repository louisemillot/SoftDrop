import uproot
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import imageio
import os
from tqdm import tqdm

def create_sequential_lund_gif(input_file, output_gif, hist_name="my-custom-task/h2_lnkt_vs_lnthetag", 
                           n_frames=100, dpi=150, fps=10):
    """
    Version finale qui :
    1. Capture TOUS les bins sans exception
    2. Garantit l'affichage des points isolés comme (9,-4)
    3. Conserve le style ROOT
    4. Offre une animation fluide
    """
    try:
        with uproot.open(input_file) as file:
            hist = file[hist_name]
            counts, x_edges, y_edges = hist.to_numpy()
            
            # 1. Paramètres visuels améliorés
            vmin = 0.9  # Affiche dès 1 count
            vmax = max(1, np.max(counts))  # Minimum 1 pour éviter les échelles vides
            
            # 2. Colormap ROOT avec blanc pour 0
            root_cmap = plt.cm.plasma
            colors = [(1,1,1,0)] + [root_cmap(i) for i in np.linspace(0, 1, 254)]
            custom_cmap = mcolors.LinearSegmentedColormap.from_list('root_white_bg', colors)
            
            # 3. Normalisation garantissant l'affichage des petits counts
            norm = mcolors.Normalize(vmin=vmin, vmax=vmax, clip=True)
            
            # 4. Extraction COMPLÈTE de tous les bins non-vides
            x_centers = (x_edges[:-1] + x_edges[1:]) / 2
            y_centers = (y_edges[:-1] + y_edges[1:]) / 2
            non_zero = np.where(counts >= 1)  # Prend tout ce qui est ≥1
            all_bins = list(zip(non_zero[0], non_zero[1], counts[non_zero]))
            
            # Diagnostic (à commenter après vérification)
            print(f"Total bins non-vides: {len(all_bins)}")
            print(f"Exemple de bins extrêmes:")
            print(f" - Coin supérieur droit: {x_centers[-1]:.1f}, {y_centers[-1]:.1f}")
            print(f" - Coin inférieur gauche: {x_centers[0]:.1f}, {y_centers[0]:.1f}")
            
            # 5. Tri précis selon X puis Y
            all_bins_sorted = sorted(all_bins, 
                                    key=lambda bin: (x_centers[bin[0]], y_centers[bin[1]]))
            
            # 6. Génération des frames avec remplissage garanti
            os.makedirs("temp_frames", exist_ok=True)
            frame_files = []
            current_hist = np.zeros_like(counts)
            
            # Nombre de bins par frame (au moins 1)
            bins_per_frame = max(1, len(all_bins_sorted) // n_frames)
            
            for i in tqdm(range(n_frames), desc="Génération des frames"):
                plt.figure(figsize=(10, 8), dpi=dpi, facecolor='white')
                
                # Détermination des bins à ajouter
                start_idx = i * bins_per_frame
                end_idx = min((i + 1) * bins_per_frame, len(all_bins_sorted))
                
                # Mise à jour de l'histogramme
                for x_idx, y_idx, cnt in all_bins_sorted[start_idx:end_idx]:
                    current_hist[x_idx, y_idx] = max(1, cnt)  # Garantit la visibilité
                
                # Affichage avec contrôle précis
                mesh = plt.pcolormesh(x_edges, y_edges, current_hist.T, 
                                     shading='auto', cmap=custom_cmap, norm=norm)
                
                # Colorbar professionnelle
                cbar = plt.colorbar(mesh, extend='both')
                cbar.set_label("Counts (log scale)", fontsize=12)
                
                # Labels et titre
                plt.xlabel("ln(1/θg)", fontsize=12)
                plt.ylabel("ln(kT)", fontsize=12)
                plt.title("Plan de Lund - Remplissage Complet\n"
                         f"Frame {i+1}/{n_frames} | Bins: {end_idx}/{len(all_bins_sorted)}", 
                         fontsize=14)
                
                # Grille et limites
                plt.grid(True, alpha=0.2, linestyle='--')
                plt.xlim(x_edges[0], x_edges[-1])
                plt.ylim(y_edges[0], y_edges[-1])
                
                # Enregistrement
                frame_file = f"temp_frames/frame_{i:03d}.png"
                plt.savefig(frame_file, bbox_inches='tight', dpi=dpi)
                plt.close()
                frame_files.append(frame_file)
            
            # 7. Création du GIF avec optimisation
            with imageio.get_writer(output_gif, mode='I', fps=fps) as writer:
                for frame in tqdm(frame_files, desc="Création du GIF"):
                    writer.append_data(imageio.v2.imread(frame))
            
            # Nettoyage
            for frame in frame_files:
                os.remove(frame)
            os.rmdir("temp_frames")
            
            print(f"\nGIF créé avec succès: {output_gif}")
            print(f"Configuration finale:")
            print(f"- Bins affichés: {np.sum(current_hist > 0)}/{len(all_bins_sorted)}")
            print(f"- Plage X: [{x_edges[0]:.2f}, {x_edges[-1]:.2f}]")
            print(f"- Plage Y: [{y_edges[0]:.2f}, {y_edges[-1]:.2f}]")
            
    except Exception as e:
        print(f"Erreur critique: {str(e)}")
        
    
if __name__ == "__main__":
    input_root_file = "PbPb_results/AnalysisResults_PbPb_LHC20e3a_R1_pt100_zcut0.1_beta0_n-1.root"
    output_gif_file = "lund_sequential_animation1.gif"
    create_sequential_lund_gif(input_root_file, output_gif_file)
    
    n_frames=100,  # Augmentation pour plus de fluidité
    fps=20,        # Accélération pour garder une durée raisonnable
    dpi=150