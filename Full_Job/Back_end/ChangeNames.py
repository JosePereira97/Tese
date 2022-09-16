from flask import json

def ChangeFileName(file, row, analyse, config):
    config = json.loads(config)
    if analyse == 'join_reads':
        ##Arranjar maneira de descobrir qual e a reversed_paired ou a forward paired. ##soluçao alterar botoes
        return file
    elif analyse == 'assembly':
        ##arranjar maniera de saber o forward e o reverse. (Assembly recebe dois files.)
        return file
    elif analyse == 'binning': ##a partir da row atualmente ja podemos saber qual o input type
        ##binning reads recebe 2 reads forward e reverse.
        ##binning contings recebe 1 por cada sample na experiments files nome vai conter so a sample buscar a config.
        return file
    elif analyse == 'recognizer':
        name = row.rsplit(' /')[0]
        for i in config['experiments']:
            if i.Name == name:
                row = i
        file = f'{row.sample}_fgs.faa'
        return file
    elif analyse == 'fastq2fasta':
        ##saber qual o forward e o reverse, cada linha recebe 2 ficheiros.
        return file
    elif analyse == 'annotation':
        ##atençao que a rule fastq2fats pode servir de inputs para o no assembly da annotation.
        name = row.rsplit(' /')[0]
        for i in config['experiments']:
            if i.Name == name:
                row = i
        if config['do_assembly']:
            file = f'{row.sample}_scaffolds.fasta'
        else:
            file = f'piled_piled_{i.Name}.fasta'
    elif analyse == 'quantification_analysis': ##sabemos qual o file type pela row
            ##quality trimmed precisamos de forward e reverse
            ##contigs por sample
            ##fgs por sample tambem
        return file
    elif analyse == 'metaphlan':
        ##problema com forward e reverse
        return file
    elif analyse == 'protein_report':
        ##UPIMAPI results tsv vem da sample
        ##recognixer results tsv vem da sample
        ##readcounts vem do name, logo e por row
        return file
    elif analyse == 'entry_report':
        ##So recebe um file
        file = 'MOSCA_Protein_Report.xlsx'
        return file
    elif analyse == 'differential_expression':
        ##recebe expression matrix dependendo da sample
        return file
    elif analyse == 'keggcharter':
        ##recebe o Mosca entry report so
        file = 'MOSCA_Entry_Report.xlsx'
        return file
    else:
        return file    