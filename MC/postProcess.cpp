#include "TFile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TCanvas.h"
#include <cmath>
#include <iostream>

void postProcess() {
    // Ouvrir le fichier ROOT contenant les histogrammes
    TFile* file = TFile::Open("PbPb_results/AnalysisResults_PbPb_LHC20e3a_R1_pt100_zcut0.1_beta0.5_n-1.root", "READ");
    if (!file || file->IsZombie()) {
        std::cerr << "Erreur : Impossible d'ouvrir le fichier PbPb_results/AnalysisResults_PbPb_LHC20e3a_R1_pt100_zcut0.1_beta0.5_n-1.root" << std::endl;
        return;
    }

    // Accéder au répertoire spécifique
    TDirectory* dir = file->GetDirectory("my-custom-task");
    if (!dir) {
        std::cerr << "Erreur : Impossible de trouver le répertoire my-custom-task" << std::endl;
        file->Close();
        return;
    }

    // Récupérer les histogrammes
    TH2F* h2_lnkt_vs_lnthetag = (TH2F*)dir->Get("h2_lnkt_vs_lnthetag");
    if (!h2_lnkt_vs_lnthetag) {
        std::cerr << "Erreur : Impossible de récupérer l'histogramme h2_lnkt_vs_lnthetag" << std::endl;
        file->Close();
        return;
    }

    // Vérifier le binning de l'histogramme original
    int nbinsX_original = h2_lnkt_vs_lnthetag->GetNbinsX();
    int nbinsY_original = h2_lnkt_vs_lnthetag->GetNbinsY();
    double xMin_original = h2_lnkt_vs_lnthetag->GetXaxis()->GetXmin();
    double xMax_original = h2_lnkt_vs_lnthetag->GetXaxis()->GetXmax();
    double yMin_original = h2_lnkt_vs_lnthetag->GetYaxis()->GetXmin();
    double yMax_original = h2_lnkt_vs_lnthetag->GetYaxis()->GetXmax();

    std::cout << "Binning de h2_lnkt_vs_lnthetag :" << std::endl;
    std::cout << "  Nombre de bins en X: " << nbinsX_original << std::endl;
    std::cout << "  Nombre de bins en Y: " << nbinsY_original << std::endl;
    std::cout << "  Limites en X: [" << xMin_original << ", " << xMax_original << "]" << std::endl;
    std::cout << "  Limites en Y: [" << yMin_original << ", " << yMax_original << "]" << std::endl;

    // Définir les valeurs seuils pour tf
    double tf1 = 0.5; // Exemple de valeur seuil
    double tf2 = 1.0; // Exemple de valeur seuil

    // Créer des histogrammes pour les événements sélectionnés avec le même binning
    TH1F* h_kt_tf1 = new TH1F("h_kt_tf1", "kT for tf < tf1", 100, 0, 10);
    TH1F* h_kt_tf2 = new TH1F("h_kt_tf2", "kT for tf < tf2", 100, 0, 10);
    TH2F* h2_lnkt_lnthetag_tf1 = new TH2F("h2_lnkt_lnthetag_tf1", "ln(kT) vs ln(1/#theta_{g}) for tf < tf1",
                                          nbinsX_original, xMin_original, xMax_original,
                                          nbinsY_original, yMin_original, yMax_original);
    TH2F* h2_lnkt_lnthetag_tf2 = new TH2F("h2_lnkt_lnthetag_tf2", "ln(kT) vs ln(1/#theta_{g}) for tf < tf2",
                                          nbinsX_original, xMin_original, xMax_original,
                                          nbinsY_original, yMin_original, yMax_original);

    // Parcourir les bins de l'histogramme 2D et appliquer les coupures
    for (int i = 1; i <= h2_lnkt_vs_lnthetag->GetNbinsX(); ++i) {
        for (int j = 1; j <= h2_lnkt_vs_lnthetag->GetNbinsY(); ++j) {
            double ln_inv_thetag = h2_lnkt_vs_lnthetag->GetXaxis()->GetBinCenter(i);
            double ln_kt = h2_lnkt_vs_lnthetag->GetYaxis()->GetBinCenter(j);
            double content = h2_lnkt_vs_lnthetag->GetBinContent(i, j);
            // std::cout << "Bin (" << i << ", " << j << ") content: " << content << std::endl;

            if (content == 0) continue;

            double thetag = 1 / exp(ln_inv_thetag);
            double kT = exp(ln_kt);
            double tf = 2.0 / (kT * thetag);

            if (tf < tf1) {
                h_kt_tf1->Fill(kT, content); // Remplir avec le contenu du bin
                h2_lnkt_lnthetag_tf1->Fill(ln_inv_thetag, ln_kt, content); // Remplir avec le contenu du bin
                std::cout << "content: " << content << std::endl;
            }

            if (tf < tf2) {
                h_kt_tf2->Fill(kT, content); // Remplir avec le contenu du bin
                h2_lnkt_lnthetag_tf2->Fill(ln_inv_thetag, ln_kt, content); // Remplir avec le contenu du bin
            }
        }
    }

    // Sauvegarder les nouveaux histogrammes dans un nouveau fichier
    TFile* outputFile = new TFile("postprocessed_histograms.root", "RECREATE");
    if (!outputFile || outputFile->IsZombie()) {
        std::cerr << "Erreur : Impossible de créer le fichier postprocessed_histograms.root" << std::endl;
        file->Close();
        return;
    }

    h_kt_tf1->Write();
    h_kt_tf2->Write();
    h2_lnkt_lnthetag_tf1->Write();
    h2_lnkt_lnthetag_tf2->Write();
    outputFile->Close();

    // Fermer le fichier d'entrée
    file->Close();
}

int main() {
    postProcess();
    return 0;
}
