import uproot
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import imageio
import os
from tqdm import tqdm

def create_sequential_lund_gif_with_jets(input_file, output_gif, hist_name="my-custom-task/h2_lnkt_vs_lnthetag",
                                         n_frames=100, dpi=150, fps=10):
    """
    Crée une animation qui visualise le remplissage du plan de Lund et la formation des jets.
    """
    try:
        with uproot.open(input_file) as file:
            hist = file[hist_name]
            counts, x_edges, y_edges = hist.to_numpy()

            # Extraire les informations sur les jets
            jet_pt = file['my-custom-task/jet_pt;1'].to_numpy()[0]
            jet_eta = file['my-custom-task/jet_eta;1'].to_numpy()[0]
            jet_phi = file['my-custom-task/jet_phi;1'].to_numpy()[0]
            zg = file['my-custom-task/zg;1'].to_numpy()[0]
            thetag = file['my-custom-task/thetag;1'].to_numpy()[0]
            kT = file['my-custom-task/kT;1'].to_numpy()[0]

            # Calculer les coordonnées dans le plan de Lund
            ln_inv_theta = np.log(1 / thetag)
            ln_kt = np.log(kT)

            # Paramètres visuels améliorés
            vmin = 0.9  # Affiche dès 1 count
            vmax = max(1, np.max(counts))  # Minimum 1 pour éviter les échelles vides

            # Colormap ROOT avec blanc pour 0
            root_cmap = plt.cm.plasma
            colors = [(1,1,1,0)] + [root_cmap(i) for i in np.linspace(0, 1, 254)]
            custom_cmap = mcolors.LinearSegmentedColormap.from_list('root_white_bg', colors)

            # Normalisation garantissant l'affichage des petits counts
            norm = mcolors.Normalize(vmin=vmin, vmax=vmax, clip=True)

            # Extraction COMPLÈTE de tous les bins non-vides
            x_centers = (x_edges[:-1] + x_edges[1:]) / 2
            y_centers = (y_edges[:-1] + y_edges[1:]) / 2
            non_zero = np.where(counts >= 1)  # Prend tout ce qui est ≥1
            all_bins = list(zip(non_zero[0], non_zero[1], counts[non_zero]))

            # Diagnostic (à commenter après vérification)
            print(f"Total bins non-vides: {len(all_bins)}")
            print(f"Exemple de bins extrêmes:")
            print(f" - Coin supérieur droit: {x_centers[-1]:.1f}, {y_centers[-1]:.1f}")
            print(f" - Coin inférieur gauche: {x_centers[0]:.1f}, {y_centers[0]:.1f}")

            # Tri précis selon X puis Y
            all_bins_sorted = sorted(all_bins,
                                     key=lambda bin: (x_centers[bin[0]], y_centers[bin[1]]))

            # Génération des frames avec remplissage garanti
            os.makedirs("temp_frames", exist_ok=True)
            frame_files = []
            current_hist = np.zeros_like(counts)

            # Nombre de bins par frame (au moins 1)
            bins_per_frame = max(1, len(all_bins_sorted) // n_frames)

            for i in tqdm(range(n_frames), desc="Génération des frames"):
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), dpi=dpi, facecolor='white')

                # Détermination des bins à ajouter
                start_idx = i * bins_per_frame
                end_idx = min((i + 1) * bins_per_frame, len(all_bins_sorted))

                # Mise à jour de l'histogramme
                for x_idx, y_idx, cnt in all_bins_sorted[start_idx:end_idx]:
                    current_hist[x_idx, y_idx] = max(1, cnt)  # Garantit la visibilité

                # Affichage avec contrôle précis
                mesh = ax1.pcolormesh(x_edges, y_edges, current_hist.T,
                                      shading='auto', cmap=custom_cmap, norm=norm)

                # Colorbar professionnelle
                cbar = plt.colorbar(mesh, ax=ax1, extend='both')
                cbar.set_label("Counts (log scale)", fontsize=12)

                # Labels et titre
                ax1.set_xlabel("ln(1/θg)", fontsize=12)
                ax1.set_ylabel("ln(kT)", fontsize=12)
                ax1.set_title("Plan de Lund - Remplissage Complet\n"
                              f"Frame {i+1}/{n_frames} | Bins: {end_idx}/{len(all_bins_sorted)}",
                              fontsize=14)

                # Grille et limites
                ax1.grid(True, alpha=0.2, linestyle='--')
                ax1.set_xlim(x_edges[0], x_edges[-1])
                ax1.set_ylim(y_edges[0], y_edges[-1])

                # Affichage des prongs
                ax2.set_xlim(0, 1)
                ax2.set_ylim(0, 1)
                ax2.set_xlabel("Prong Index", fontsize=12)
                ax2.set_ylabel("Depth", fontsize=12)
                ax2.set_title("Formation des Jets", fontsize=14)
                ax2.grid(True, alpha=0.2, linestyle='--')

                # Exemple de représentation des prongs
                # Vous devrez ajuster cette partie en fonction de la structure de vos données
                for j in range(end_idx):
                    ax2.plot([0, 1], [j/n_frames, (j+1)/n_frames], marker='o', color='blue', alpha=0.5)

                # Enregistrement
                frame_file = f"temp_frames/frame_{i:03d}.png"
                plt.savefig(frame_file, bbox_inches='tight', dpi=dpi)
                plt.close()
                frame_files.append(frame_file)

            # Création du GIF avec optimisation
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
    output_gif_file = "lund_sequential_animation_with_jets.gif"
    create_sequential_lund_gif_with_jets(input_root_file, output_gif_file, n_frames=100, fps=20, dpi=150)
