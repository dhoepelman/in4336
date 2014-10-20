#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * C code genereert een LP bestand uit een DIGRAPH
 * Dit LP bestand draait vervolgens in GUROBI


 * Aanroep: gc_to_ilp k
 * k = k van k-GC
 */

int main(int argc, char *argv[])
{
    int k;

    //k = atoi(argv[1]);

    FILE *infile;
    char str[60];

    /* opening file for reading */
    infile=fopen("1-Fulllns_3.col", "r");
    if(infile == NULL) {
      perror("Error opening file");
      return(-1);
    }
    char c;
    char str2[4]="0000";
    char str3[4]="0000";

    int vertices=0, edges=0;
    int v1[1000], v2[1000];
    int i,j,l=1;

    /* lees het aantal vertices en edges uit het *.col bestand */
    while (fscanf(infile, "%s", str) != EOF) {
        //printf("%s", str);
        if(str[0] == 'p') {
            fscanf(infile, "%s %d %d", str2, &vertices, &edges);
            printf("str2=%s, vertices=%d, edges=%d\n",str2,vertices,edges);
	    k = vertices;
        }
        else if(str[0] == 'e')
        {
            fscanf(infile, "%d %d", &v1[l], &v2[l]);
            //printf("v1[%d]=%d, v2[%d]=%d\n", l, v1[l], l, v2[l]);
            l++;
        }
    }
    fclose(infile);


    // opening file for writing
    FILE *outfile;
    outfile=fopen("gc2.lp", "w+");
    if(outfile == NULL) {
      perror("Error opening file");
      return(-1);
    }

    /**/
    fprintf(outfile, "Minimize\n\ty1");
    for(i=2; i<=k; i++) {
        fprintf(outfile, " + y%i", i);
    }

    j=1;
    fprintf(outfile, "\nSubject To\n");
    // Zorg dat elke vertex precies één kleur heeft
    for(i=1; i<=vertices; i++) {
        fprintf(outfile, "\tv%i: x%i_%i", i, i, j);
        for(j=2; j<=k; j++) {
            fprintf(outfile, " + x%d_%d", i, j);
        }
        fprintf(outfile, " = 1\n");
        j=1;
    }
    
    l=1;
    
    // Zorg dat nodes geen kleur krijgen die niet gebruikt wordt
    for(i=1; i<=vertices; i++) {
        fprintf(outfile, "\n");
        for(j=1; j<=k; j++) {
            fprintf(outfile, "\td%i: x%i_%i - y%i <= 0", l, i, j, j);
            l++;
            fprintf(outfile, "\n");
        }
    }
    l=1;
    fprintf(outfile, "\n");
    
    // Zorg dat nodes die met een edge verbonden zijn niet dezelfde kleur krijgen
    for(i=1; i<=edges; i++) {
        for(j=1; j<=k; j++) {
            fprintf(outfile, "\te%i: x%i_%i + x%i_%i <= 1\n", l, v1[i], j, v2[i], j);
            l++;
        }
        fprintf(outfile, "\n");
    }
    
    // Zorg dat alle variabelen 0 of 1 zijn
    fprintf(outfile, "Bounds\n");
    for(i=1; i<=vertices; i++) {
        for(j=1; j<=k; j++) {
            fprintf(outfile, "\t0 <= x%i_%i <= 1\n", i, j);
        }
    }
    fprintf(outfile, "\n");
    for(i=1; i<=k; i++) {
            fprintf(outfile, "\t0 <= y%i <= 1\n", i);
    }
    
    // Zorg dat alle variabelen integeres zijn
    fprintf(outfile, "Integers\n\t");
    for(i=1; i<=vertices; i++) {
        for(j=1; j<=k; j++) {
            fprintf(outfile, "x%i_%i ", i, j);
        }
    }
    for(i=1; i<=k; i++) {
            fprintf(outfile, "y%i ", i);
    }
    fprintf(outfile, "\nEnd\n");
    fclose(outfile);
    return 0;
}
