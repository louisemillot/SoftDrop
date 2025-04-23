void plot_histogram() {
    // Ouvrir le fichier ROOT
    TFile *file = TFile::Open("PbPb_results/AnalysisResults_PbPb_LHC20e3a_R1_pt100_zcut0.1_beta0.5_n-1.root");
    if (!file || file->IsZombie()) {
        std::cerr << "Erreur: Impossible d'ouvrir AnalysisResults.root" << std::endl;
        return;
    }

    // Accéder au répertoire my-custom-task
    TDirectory *dir = (TDirectory*)file->Get("my-custom-task");
    if (!dir) {
        std::cerr << "Erreur: Répertoire my-custom-task introuvable" << std::endl;
        file->Close();
        return;
    }

    // Récupérer l'histogramme 2D
    TH2D *h = (TH2D*)dir->Get("h2_lnkt_vs_lnthetag;1");
    if (!h) {
        std::cerr << "Erreur: Histogramme h2_lnkt_vs_lnthetag;1 introuvable" << std::endl;
        file->Close();
        return;
    }

    // Créer un canvas et dessiner l'histogramme
    TCanvas *c = new TCanvas("c", "h2_lnkt_vs_lnthetag", 800, 600);
    
    gStyle->SetOptStat(1111);  // 1111 = active mean/RMS/entries/etc.
    gStyle->SetStatX(0.9);     // Position X (0-1)
    gStyle->SetStatY(0.9);     // Position Y
    gStyle->SetStatW(0.2);     // Largeur
    gStyle->SetStatH(0.1);     // Hauteur
    h->Draw("COLZ");

    // Sauvegarder en PNG et PDF
    c->SaveAs("h2_lnkt_vs_lnthetag.png");
    c->SaveAs("h2_lnkt_vs_lnthetag.pdf");

    // Fermer le fichier
    file->Close();
}