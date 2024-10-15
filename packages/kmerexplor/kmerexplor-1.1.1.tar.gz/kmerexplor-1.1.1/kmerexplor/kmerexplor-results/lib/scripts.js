// These 3 lines aim to refresh chart when the "chart_content" div is resized
var myChart = echarts.init(document.getElementById("chart_content"),);
window.addEventListener("resize", function(event){myChart.resize();});
function resizeChart() {myChart.resize()}

// Manage sliding sidenav
function hideElement() {var x = document.getElementById("Sidenav"); var hideIcon = document.getElementById("hide-icon");if (x.style.width === "0px") {x.style.width = "250px";document.getElementById("main").style.marginLeft = "250px";hideIcon.innerHTML = "&#9664";} else {x.style.width = "0";document.getElementById("main").style.marginLeft= "0";hideIcon.innerHTML = "&#9654";};setTimeout(resizeChart, 500);}

// Samples array variable
var samples = ['Samples', 'A', 'B', 'C', 'D', 'E'];
var samples_as_fastq = ['Samples', 'A_1', 'A_2', 'B_1', 'B_2', 'C_1', 'C_2', 'D_1', 'D_2', 'E_1', 'E_2'];

// metadata and dataset to build graph
var _Histones = {
    chart_type: 'bar',
    theme: 'light',
    threshold: [{yAxis:200,}],
    yAxis_max: 200,
    toolbox_type: ['stack', 'tiled'],
    title_text: "Poly A and Ribo depletion by Histone detection",
    show_fastq: false,
    legend_padding_top: [40, 30, 0, 30],
    grid_top: '28%',
    nb_seqId: 32,
    dataset: [
                [],
                ['HIST1H1A', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H1B', 0.0, 0.0, 7.553, 0.0, 0.0],
                ['HIST1H1D', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H1E', 5.417, 0.0, 0.0, 0.0, 5.579],
                ['HIST1H1T', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H2AB', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H2AG', 2.217, 4.175, 0.0, 0.0, 2.088],
                ['HIST1H2AH', 0.0, 0.0, 12.22, 0.0, 0.0],
                ['HIST1H2BA', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H2BB', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H2BE', 2.704, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H2BF', 0.0, 0.0, 0.0, 2.955, 0.0],
                ['HIST1H2BH', 0.0, 0.0, 0.0, 1.313, 0.0],
                ['HIST1H2BL', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H2BM', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H2BN', 0.0, 5.51, 0.0, 0.0, 0.0],
                ['HIST1H3A', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H3B', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H3C', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H3E', 0.0, 0.0, 0.0, 0.0, 1.62],
                ['HIST1H3F', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H3G', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H3H', 3.339, 1.407, 0.0, 3.339, 0.0],
                ['HIST1H3I', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H4B', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H4C', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H4D', 12.67, 5.429, 0.0, 0.0, 0.0],
                ['HIST1H4F', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST1H4I', 3.35, 10.5, 2.114, 3.665, 5.217],
                ['HIST1H4J', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['HIST2H2AB', 0.0, 0.0, 10.07, 0.0, 0.0],
                ['HIST2H2AC', 4.179, 0.0, 12.16, 11.14, 0.0],
    ],
    desc: [
        "Poly A selection",
        "<strong>Predictor genes selection:</strong> when total RNA is extracted from a human sample, the most abundant component is ribosomal RNA (rRNA, 80 to 90%, <em>O'Neil et al. (2013)</em>), which must be removed to measure gene/transcript abundances using RNA-seq technology. Commonly used protocols to remove rRNA are polyadenylated mRNA selection (polyA+) and ribo-depletion (Ribo-Zero). To differentiate these 2 protocols, we selected widely expressed histone genes which produce non-polyadenylated transcripts barely detected into polyA+ RNA-seq. These predictor genes are listed in the legend.",
        "<strong>Specific k-mers quantification:</strong> several specific k-mers designed with Kmerator are associated to each selected histone gene. KmerExploR uses countTags to compute k-mer occurrences number in each RNA-seq sample and calculates the mean count value for each gene (Y axis, mean k-mer counts normalized per billion of k-mers).",
        "<strong>Threshold :</strong> the threshold was defined based on several RNA-seq datasets but might not fit perfectly your data. Ribo-depleted samples should be above the threshold and polyA+ below."
    ]
};


// metadata and dataset to build graph
var _Orientation = {
    chart_type: 'bar',
    theme: 'light',
    threshold: false,
    yAxis_max: null,
    toolbox_type: ['stack', 'tiled'],
    title_text: "Orientation",
    show_fastq: true,
    legend_padding_top: [40, 30, 0, 30],
    grid_top: '16%',
    nb_seqId: 20,
    dataset: [
                ['C1orf43', 0.0, 143.8, 0.0, 138.7, 0.0, 163.4, 0.0, 151.5, 1.438, 209.1],
                ['C1orf43', -147.0, -0.0, -138.9, -0.0, -174.3, -0.0, -157.4, -0.0, -214.3, -1.458],
                ['CHMP2A', 0.0, 44.86, 0.0, 58.51, 0.0, 50.19, 0.0, 48.69, 0.9791, 44.78],
                ['CHMP2A', -45.07, -0.0, -69.54, -0.0, -61.57, -0.0, -58.83, -0.0, -47.25, -3.484],
                ['EMC7', 0.0, 65.91, 0.0, 43.22, 0.0, 62.12, 0.0, 43.02, 0.0, 69.58],
                ['EMC7', -69.11, -0.0, -39.67, -0.0, -64.56, -0.0, -43.9, -0.0, -69.23, -0.0],
                ['GPI', 0.0, 96.92, 0.0, 115.4, 0.0, 78.09, 0.0, 63.57, 0.0, 101.6],
                ['GPI', -101.9, -0.0, -113.4, -0.0, -85.32, -0.0, -66.47, -1.038, -104.6, -0.0],
                ['PSMB2', 0.0, 60.51, 0.0, 28.65, 0.0, 52.38, 0.0, 64.63, 0.0, 64.92],
                ['PSMB2', -61.85, -0.0, -29.98, -0.0, -53.76, -0.0, -68.69, -0.0, -68.28, -0.0],
                ['PSMB4', 0.0, 453.8, 0.0, 405.1, 0.0, 363.1, 0.0, 397.4, 4.283, 423.9],
                ['PSMB4', -480.9, -0.0, -387.2, -0.0, -384.5, -0.0, -392.8, -0.0, -442.3, -3.752],
                ['RAB7A', 0.0, 117.4, 0.0, 104.6, 0.0, 91.83, 0.0, 103.4, 0.0, 97.58],
                ['RAB7A', -121.3, -0.3903, -109.5, -0.0, -100.8, -0.0, -102.5, -0.0, -100.9, -0.0],
                ['REEP5', 0.0, 65.61, 0.0, 34.1, 1.214, 28.65, 0.0, 36.1, 0.0, 28.6],
                ['REEP5', -65.71, -0.0, -33.08, -0.0, -31.96, -1.224, -38.02, -0.0, -30.55, -0.0],
                ['SNRPD3', 0.0, 57.3, 0.0, 85.19, 0.0, 82.59, 0.0, 70.22, 0.0, 48.36],
                ['SNRPD3', -59.41, -0.0, -85.93, -0.0, -80.16, -0.0, -67.65, -0.0, -49.64, -0.0],
                ['VPS29', 0.0, 52.75, 0.0, 47.96, 0.0, 31.7, 3.035, 28.57, 0.0, 53.52],
                ['VPS29', -69.5, -0.0, -55.21, -0.0, -38.4, -0.0, -41.89, -2.734, -61.12, -0.0],
    ],
    desc: [
        "Orientation",
        "<strong>Predictor genes selection:</strong> paired-end RNA-seq protocol generates 2 fastq files per sample. To determine the orientation of these files (stranded/unstranded) we selected a subset of housekeeping genes from the list previously published by Eisenberg and Levanon (<em>Eisenberg et al. (2013)</em>). These predictor genes are listed in the legend.",
        "<strong>Specific k-mers quantification and interpretation:</strong> for each predictor gene, we designed specific k-mers with Kmerator and also computed these k-mers reverse-complements. With KmerExploR, forward specific k-mers are counted as positive (Y axis, mean k-mer counts normalized per billion of k-mers), and their reverse-complements are counted as negative. For each predictor gene and both forward and reverse counts, the mean value is calculated. When the samples are stranded, forward and reverse k-mers are expected to be respectively in 2 different fastq files. If  forward and reverse k-mers are equally found in each fastq file (balanced positive and negative counts) the sample is considered as unstranded."
    ]
};


// metadata and dataset to build graph
var _Gender = {
    chart_type: 'bar',
    theme: 'light',
    threshold: [{yAxis:5,}],
    yAxis_max: 5,
    toolbox_type: ['stack', 'tiled'],
    title_text: "Y chromosome detection",
    show_fastq: false,
    legend_padding_top: [40, 30, 0, 30],
    grid_top: '17%',
    nb_seqId: 7,
    dataset: [
                [],
                ['DDX3Y', 0.0, 0.0, 0.0, 0.0, 0.02031],
                ['EIF1AY', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['NLGN4Y', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['RPS4Y1', 0.0, 0.0, 0.0, 0.0, 0.04253],
                ['TBL1Y', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['TMSB4Y', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['UTY', 0.0, 0.0, 0.0, 0.0, 0.0],
    ],
    desc: [
        "Gender",
        "<strong>Predictor genes selection:</strong> to determine the gender, we selected previously published chromosome Y specific genes (<em>A. A. Maan et al. (2017)</em>) that have an ubiquitous expression. These predictor genes are listed in the legend.",
        "<strong>Specific k-mers quantification and interpretation:</strong> several specific k-mers designed with Kmerator are associated to each selected chromosome Y gene. KmerExploR uses countTags to compute k-mer occurrences number in each RNA-seq sample and calculates the mean count value for each gene (Y axis, mean k-mer counts normalized per billion of k-mers). Females should have an almost zero expression for all selected genes contrary to males that should express them all."
    ]
};


// metadata and dataset to build graph
var _Read_biases = {
    chart_type: 'bar',
    theme: 'light',
    threshold: false,
    yAxis_max: 100,
    toolbox_type: ['stack', 'tiled'],
    title_text: "Read position biases",
    show_fastq: false,
    legend_padding_top: [40, 30, 0, 30],
    grid_top: '15%',
    nb_seqId: 3,
    dataset: [
                ['3"UTR', 21.04, 17.95, 16.79, 17.9, 17.46],
                ['CDS', 66.85, 57.74, 60.82, 61.28, 58.63],
                ['5"UTR', 12.11, 24.31, 22.38, 20.81, 23.9],
    ],
    desc: [
        "Read position biases",
        "<strong>Predictor genes selection:</strong> read coverage bias from 5' to 3' end can be one important parameter to analyse. Indeed, if reads primarily accumulate at the 3’ end of transcripts in poly(A)-selected samples, this might also indicate low RNA quality in the starting material (<em>Conesa et al. (2016)</em>). During mapping process, tools for quality control are used including Picard, RSeQC and Qualimap. Here, to check the uniformity of read coverage, we selected a subset of housekeeping genes from the list previously published by Eisenberg and Levanon (<em>Eisenberg et al. (2013)</em>) : VPS29, SNRPD3, REEP5, RAB7A, PSMB4, PSMB2, GPI, EMC7, CHMP2A and C1orf43.",
        "<strong>Specific k-mers quantification and interpretation:</strong> for each predictor gene, we designed specific k-mers with Kmerator and distinguished the mean k-mer counts from 5', 3' and CDS regions. Results are presented, for each sample, with the cumulative mean of each region (all predictor gene mean counts are grouped together by region), reported as a percentage (Y axis). In absence of bias, one can expect a conserved proportion of the corresponding region among samples. Conversely, if a bias is present in the data this proportion will be lost."
    ]
};


// metadata and dataset to build graph
var _HeLa_HPV18 = {
    chart_type: 'bar',
    theme: 'light',
    threshold: [{yAxis:10,}],
    yAxis_max: 10,
    toolbox_type: ['stack', 'tiled'],
    title_text: "Hela HPV18",
    show_fastq: false,
    legend_padding_top: [40, 30, 0, 30],
    grid_top: '22%',
    nb_seqId: 19,
    dataset: [
                [],
                ['E1_mut1012', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['E1_mut1353', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['E1_mut1807', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['E1_mut1843', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['E1_mut1994', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['E1_mut2269', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['E6_mut104', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['E6_mut287', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['E6_mut485', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['E6_mut549', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['E7_mut751', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['E7_mut806', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['L1_mut5875', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['L1_mut6401', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['L1_mut6460', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['L1_mut6625', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['L1_mut6842', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['L1_mut7258', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['L1_mut7486', 0.0, 0.0, 0.0, 0.0, 0.0],
    ],
    desc: [
        "Hela contamination",
        "<strong>Predictor genes selection:</strong> HeLa is the first immortal human cell line, coming from Henrietta Lacks cancerous tissue samples. Her cancer was triggered by an infection with human papillomavirus type 18 (HPV-18). Nowadays, this cell line is largely used in medical research and HeLa contaminations in other cell types have been observed (<em>Selitsky et al. (2020)</em>). 3 segments of HPV-18 are integrated into HeLa genome on chromosome 8 and include the long control region (LCR), the E6, E7 and E1 genes, and partial coding regions for the E2 and L1 genes (<em>Cantalupo et al. (2015)</em>). From these genes expressed in HeLa cells with specific mutations (<em>Cantalupo et al. (2015)</em>), we selected 60 nt long sequences around each mutation. These predictor gene specific mutations are listed in the legend.",
        "<strong>Specific k-mers quantification and interpretation:</strong> for each selected HeLa specific mutation 60 nt sequence, we designed specific k-mers with Kmerator. Next, KmerExploR uses countTags to compute k-mer occurrences number in each RNA-seq sample and calculates the mean count value for each selected HeLa specific mutation (Y axis, mean k-mer counts normalized per billion of k-mers). Using this quantification, we are able to highlight potential HeLa contamination."
    ]
};


// metadata and dataset to build graph
var _Mycoplasma = {
    chart_type: 'bar',
    theme: 'light',
    threshold: [{yAxis:20,}],
    yAxis_max: 20,
    toolbox_type: ['stack', 'tiled'],
    title_text: "Mycoplasma",
    show_fastq: false,
    legend_padding_top: [40, 30, 0, 30],
    grid_top: '16%',
    nb_seqId: 6,
    dataset: [
                [],
                ['Acholeplasma_laidlawii', 0.4959, 0.9213, 1.152, 1.826, 0.7289],
                ['Mycoplasma_arginini', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Mycoplasma_fermentans', 0.085, 0.3103, 0.0765, 0.357, 0.17],
                ['Mycoplasma_hominis', 0.02486, 0.0, 0.0, 0.0, 0.0],
                ['Mycoplasma_hyorhinis', 0.02961, 0.01776, 0.0, 0.02665, 0.1036],
                ['Mycoplasma_orale', 0.0, 0.0, 0.4315, 0.1501, 0.1376],
    ],
    desc: [
        "Mycoplasma contamination",
        "<strong>Predictor genes selection:</strong> mycoplasma is a common source of cell culture sample contamination and can affect  gene expression. To control  its presence in RNA-seq data, we checked for the most frequent mycoplasma found in cell contamination, according to <em>Drexler et al. (2002)</em>.  For each of the 6 selected mycoplasma species (A. laidlawii, M. fermentans, M. hominis, M. hyorhinis, M. orale and M. arginini; also listed in the legend), we downloaded the 16S ribosomal RNA sequences. Indeed, according to the literature, 90% of the specific mycoplasma-mapped reads from human RNA-seq samples mapped to mycoplasma ribosomal RNA (<em>Olarerin-George et al. (2015)</em>).",
        "<strong>Specific k-mers quantification:</strong> specific k-mers were designed for each of 6 mycoplasma species’ rRNA sequences using Kmerator. Next, KmerExploR uses countTags to compute k-mer occurrences number in each RNA-seq sample and calculates the mean count value for each mycoplasma specie (Y axis, mean k-mer counts normalized per billion of k-mers).",
        "<strong>Threshold:</strong> the threshold is an indication: above it, we could consider the sample as contaminated by mycoplasms. "
    ]
};


// metadata and dataset to build graph
var _Virus_genome = {
    chart_type: 'bar',
    theme: 'light',
    threshold: [{yAxis:1,}],
    yAxis_max: null,
    toolbox_type: ['stack', 'tiled'],
    title_text: "Virus detection",
    show_fastq: false,
    legend_padding_top: [40, 30, 0, 30],
    grid_top: '20%',
    nb_seqId: 14,
    dataset: [
                [],
                ['Bovine_viral_diarrhea_virus', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Hepatitis_B_virus_strain', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Hepatitis_C_virus_genotype', 0.0, 0.0, 0.0, 0.0, 0.006926],
                ['Human_T_lymphotropic_virus_1', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Human_T_lymphotropic_virus_2', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Human_gammaherpesvirus_4', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Human_herpesvirus_4', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Human_herpesvirus_8', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Human_immunodeficiency_virus_1', 61.83, 70.79, 36.7, 46.66, 47.25],
                ['Human_immunodeficiency_virus_2', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Human_papillomavirus_type_92', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['MuLV_related_virus_22Rv1slashCWR', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Murine_leukemia_virus', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Squirrel_monkey_retrovirus', 0.0, 0.0, 0.0, 0.0, 0.0],
    ],
    desc: [
        "Viruses contamination",
        "<strong>Predictor genes selection:</strong> viruses are a significant cause of human cancers. In a recent study, <em>Uphoff et al. (2019)</em> screened more than 300 Cancer Cell Line Encyclopedia RNA-seq and revealed 20 infected cell lines with different viruses. To rapidly explore the potential presence of viruses into RNA-seq datasets, we used the 14 viruses reference genomes described in <em>Uphoff et al.</em> Study. These viruses are listed in the legend.",
        "<strong>Specific k-mers quantification and interpretation:</strong> we used Kmerator to select, for each virus, the k-mers absent from the human reference genome and transcriptome. Next, KmerExploR uses countTags to compute k-mer occurrences number in each RNA-seq sample and calculates the mean count value for each virus (Y axis, mean k-mer counts normalized per billion of k-mers). Using this quantification, we are able to highlight potential common viruses contamination."
    ]
};


// metadata and dataset to build graph
var _Specie = {
    chart_type: 'bar',
    theme: 'light',
    threshold: false,
    yAxis_max: 100,
    toolbox_type: ['stack', 'tiled'],
    title_text: "Ensembl species",
    show_fastq: false,
    legend_padding_top: [40, 30, 0, 30],
    grid_top: '19%',
    nb_seqId: 11,
    dataset: [
                ['Homo_sapiens_MT_CO1', 99.49, 99.58, 99.58, 99.62, 99.65],
                ['Caenorabditis_elegans_ctc_3_MTCE', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Caenorabditis_elegans_ctc', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Drosophila_melanogaster_mt_CoI', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Rattus_norvegicus_Mt_co1', 0.51, 0.42, 0.42, 0.38, 0.35],
                ['arabidopsis_thaliana_COX1', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Zea_mays_COX1', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Gallus_gallus_MT_CO1', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Mus_musculus_mt_Co1', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Danio_rerio_mt_co1', 0.0, 0.0, 0.0, 0.0, 0.0],
                ['Saccharomyces_cerevisiae_COX1', 0.0, 0.0, 0.0, 0.0, 0.0],
    ],
    desc: [
        "Species",
        "<strong>Predictor genes selection:</strong> the probability of mixed cell lines in samples preparation, usage of polymerase chain reaction (PCR) which can accidentally amplify the wrong piece of DNA, plus an unknown probability of error in metadata assignation motivated us to check the species present in an RNA-seq sample. Based on several studies, the mitochondrially encoded cytochrome c oxidase I (MT-CO1) is a gene marker that could be sufficient for a quick check of the specie of an RNA-seq sample (<em>Hebert et al. (2003)</em>). Indeed, this gene is highly expressed and reference sequences from many distinct species are available. Thus, we selected the MT-CO1 gene from 10 different species. These species are listed in the legend.",
        "<strong>Specific k-mers quantification:</strong> with Kmerator, we designed specific k-mers for each MT-CO1 ortholog, using the appropriate specie reference genome and transcriptome. Next, KmerExploR uses countTags to compute k-mer occurrences number in each RNA-seq sample and calculates the mean count value for each specie (Y axis, mean k-mer counts normalized per billion of k-mers). "
    ]
};

// Define serie for chartjs() function
function set_series(category) {
    if (typeof category.stack == 'undefined') {
        category.stack = 'one';
    };
    /* Build series Object for chartjs() */
    series = [];
    if (category.threshold) {
        series.push({type: 'line', seriesLayoutBy: 'row', markLine: {symbol: 'none', label: {show: true,formatter: 'Threshold'},lineStyle: {width: 2, opacity: 0.6}, data: category.threshold}});
    };
    for (i=0, c=category.nb_seqId; i<c; i++) {
        series.push({type: category.chart_type, stack: category.stack, seriesLayoutBy: 'row'});
    }
    return series
}

// chartjs() draw chart using values from one category and set_series() function
function chartjs(category) {
    // clear home content
    home_html = document.getElementById('home_content');
    home_html.innerHTML = '';
    // weight of chart content
    chart_html = document.getElementById('chart_content');
    chart_html.style.height = '600px';
    // set series (same object * categories count)
    series = set_series(category);
    // dataset = samples + dataset
    if (category.dataset[0][0] != 'Samples') {
        if (category.show_fastq) {
            category.dataset.unshift(samples_as_fastq);
        } else {
            category.dataset.unshift(samples);
        };
    };
    // clear charts
    echarts.dispose(document.getElementById('chart_content'));
    // init chart
    myChart = echarts.init(
        document.getElementById('chart_content'),
        category.theme,
    );
    // specify chart configuration item and data
    var option = {
        dataset: {
            source: category.dataset
        },
        title: {text: category.title_text},
        toolbox: {
            feature: {
                magicType: {type: category.toolbox_type},
                dataZoom: {yAxisIndex: false},
                saveAsImage: {pixelRatio: 2}
            }
        },
        tooltip: {},
        emphasis: {focus: 'series'},
        legend: {
          padding: [40, 30, 0, 30],
          selector: true,
        },
        dataZoom: [{
                type: 'inside',
            }],
        grid: {
            top: category.grid_top
        },
        xAxis: {type: 'category'},
        yAxis: {max: category.yAxis_max},
        series: series,
    };
    myChart.setOption(option);

    // Add Description;
    description(category);
};

// Set the description of the category in "desc_content" div id
function description(category) {
    var desc = category.desc;
    desc_html = document.getElementById("desc_content");
    desc_html.innerHTML = "";
    for (i=0; i<desc.length; i++) {
        if (i==0) {
            desc_html.innerHTML += "<h2>" + desc[i] + "</h2>";
        } else {
            desc_html.innerHTML += "<p>" + desc[i] + "</p>";
        }
    }
}

// Home page
function home() {
    // clear home content
    home_html = document.getElementById('home_content');
    home_html.innerHTML = '';
    // clear charts
    chart_html = document.getElementById('chart_content');
    chart_html.innerHTML = '';
    chart_html.style.height = 0;
    // clear chart description
    desc_html = document.getElementById('desc_content');
    desc_html.innerHTML = '';
    // content of Home page
    home_html.innerHTML += "<p>Mode: paired</p><p>KmerExploR version: 1.1.0</p><details><p><summary>5 samples analysed</summary></p><p>A - B - C - D - E</p></details>";
    home_html.innerHTML += "<details><p><summary>About fastq files</summary></p><table id='fastq-info'><tbody><tr><th>Fastq file</th><th>number of kmers</th><th>number of reads</th></tr><tr><td>A_1</td><td>30250000</td><td>1000000</td></tr><tr><td>A_2</td><td>30250000</td><td>1000000</td></tr><tr><td>B_1</td><td>30250000</td><td>1000000</td></tr><tr><td>B_2</td><td>30250000</td><td>1000000</td></tr><tr><td>C_1</td><td>30250000</td><td>1000000</td></tr><tr><td>C_2</td><td>30250000</td><td>1000000</td></tr><tr><td>D_1</td><td>30250000</td><td>1000000</td></tr><tr><td>D_2</td><td>30250000</td><td>1000000</td></tr><tr><td>E_1</td><td>30250000</td><td>1000000</td></tr><tr><td>E_2</td><td>30250000</td><td>1000000</td></tr><tr><td>Total</td><td>302500000</td><td>10000000</td></tr></tbody></table></details>";
    home_html.innerHTML += '<hr />';
    home_html.innerHTML += "<p><strong>KmerExploR</strong> visualization of your RNA-seq basic features is separated into several sections/subsections:</p><p><strong>Basic Features</strong></p><ul><li>Poly A / Ribo D: are my RNA-seq data based on poly-A selection protocol or ribo-depletion ?</li><li>Orientation: are my RNA-seq libraries stranded or not ?</li><li>Y chromosome: what is/are the gender(s) corresponding to my samples ?</li><li>Read position biases: is there a read coverage bias from 5' to 3' ends ?</li></ul><p><strong>Contamination</strong></p><ul><li>HeLa: are my RNA-seq data contaminated by HeLa (presence of HeLa-derived human papillomavirus 18) ?</li><li>Mycoplasma: are my RNA-seq data contaminated by mycoplasmas ?</li><li>Virus: are my RNA-seq data contaminated by viruses such as hepatitis B virus ?</li><li>Species: what is/are the species present into my samples ?</li></ul><p>For each subsection, a graph shows the quantification of predictor genes (Y axis, mean k-mer counts normalized per billion of k-mers in the sample) in each RNA-seq sample of your dataset (X axis). More details on the predictor genes and their selection to answer a specific biological question are described into the corresponding subsections.</p><p><em>Citation: <a href='https://pubmed.ncbi.nlm.nih.gov/34179780/' target='_blank'>Kmerator Suite</a>.</em></p>";
    };
