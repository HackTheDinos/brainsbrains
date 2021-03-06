#include "buildTwoLayerTriangles.h"
#include <stdio.h>

void buildTwoLayerTriangles(void * resultsv, void * l1v, int n1, int z1, void * l2v, int n2, int z2) {
    int * l1_flat = (int *) l1v;
    int * l2_flat = (int *) l2v;

    // restructure flat input to a multidimensional array
    int l1[n1][2];
    int l2[n2][2];
    int i;
    for(i=0; i<n1; i++) {
        l1[i][0] = l1_flat[i*2];
        l1[i][1] = l1_flat[i*2+1];

        int j;
        for(j=0; j<i; j++) {
            if(l1[i][0] == l1[j][0] && l1[i][1] == l1[j][1]) {
                printf("duplicate boundary point - l1[%d] and l1[%d] are both (%d, %d)\n", j, i, l1[i][0], l1[i][1]);
            }
        }
    }

    for(i=0; i<n2; i++) {
        l2[i][0] = l2_flat[i*2];
        l2[i][1] = l2_flat[i*2+1];

        int j;
        for(j=0; j<i; j++) {
            if(l2[i][0] == l2[j][0] && l2[i][1] == l2[j][1]) {
                printf("duplicate boundary point - l2[%d] and l2[%d] are both (%d, %d)\n", j, i, l2[i][0], l2[i][1]);
            }
        }

    }

    // do triangle generation
    int triangles[n1+n2][3][3];  // results will go here
    generateTriangles(triangles, l1, n1, z1, l2, n2, z2);

    // flatten multidimensional results array
    int *triangles_flat = (int *) resultsv;
    int j,k;
    for(i=0; i<n1+n2; i++)
        for(j=0; j<3; j++)
            for(k=0; k<3; k++)
                triangles_flat[i*9 + j*3 + k] = triangles[i][j][k];

}

void generateTriangles(int triangles[][3][3], int l1[][2], int n1, int z1, int l2[][2], int n2, int z2) {
    /*
     * This function expects a set of ordered points from two layers (l1, l2) that define the
     * boundaries of the areas of interest. number of points (n1, n2) and z position for each slice
     * (z1, z2) must also be provided. The first argument points to the array created to store 
     * the resulting triangles and should have a length of n1+n2
     *
     * triangles are generated by starting with closely matching points on the boundary of each
     * layer's area. The optimal 3rd point to form a triangle is then chosen by minimizing the
     * hypotenuse distance between available options. This proceedure is then iterated moving
     * forward around each layer's boundary (one point at a time) until triangles have been formed
     * for the entire perimiter.
     */

    int done = 0; 
    int i1 = 0;
    int i2 = 0;

    while(!done) {
        int start_i1 = i1;
        int start_i2 = i2;

        if(i1<n1-1 && i2<n2-1) {
            int d12 = getDist(l1[i1], l2[i2+1]);
            int d21 = getDist(l2[i2], l1[i1+1]);

            if(d12 < d21) {
               addTriangle(n1, i1, n2, i2, triangles[i1+i2], l1[i1], z1, l2[i2], z2, l2[i2+1], z2);
               i2++;
            } else {
               addTriangle(n1, i1, n2, i2, triangles[i1+i2], l1[i1], z1, l2[i2], z2, l1[i1+1], z1);
               i1++;
            }
        } else if(i2<n2-1) {
           addTriangle(n1, i1, n2, i2, triangles[i1+i2], l1[i1], z1, l2[i2], z2, l2[i2+1], z2);
           i2++;
        } else if(i1<n1-1) {
           addTriangle(n1, i1, n2, i2, triangles[i1+i2], l1[i1], z1, l2[i2], z2, l1[i1+1], z1);
           i1++;
        } else {
            int d12 = getDist(l1[i1], l2[0]);
            int d21 = getDist(l2[i2], l1[0]);

            if(d12 < d21) {
               addTriangle(n1, i1, n2, i2, triangles[i1+i2], l1[i1], z1, l2[i2], z2, l2[0], z2);
               addTriangle(n1, i1, n2, i2, triangles[i1+i2+1], l1[i1], z1, l2[0], z2, l1[0], z1);
            } else {
               addTriangle(n1, i1, n2, i2, triangles[i1+i2], l1[i1], z1, l2[i2], z2, l1[0], z1);
               addTriangle(n1, i1, n2, i2, triangles[i1+i2+1], l1[0], z1, l2[i2], z2, l2[0], z2);
            }
            done = 1;
        }
    }
}

void addTriangle(int n1, int i1, int n2, int i2, int triangle[][3], int xy1[2], int z1, int xy2[2], int z2, int xy3[2], int z3) {
    int dupvert = 0;
    int which_unique;
    int dupvalues[3];

    if((xy1[0] == xy2[0]) && (xy1[1] == xy2[1]) && (z1 == z2)) {
        dupvert = 1;
        which_unique = 3;
        dupvalues[0] = xy1[0];
        dupvalues[1] = xy1[1];
        dupvalues[2] = z1;
    }


    if((xy3[0] == xy2[0]) && (xy3[1] == xy2[1]) && (z3 == z2)) {
        dupvert = 1;
        which_unique = 1;
        dupvalues[0] = xy3[0];
        dupvalues[1] = xy3[1];
        dupvalues[2] = z3;
    }

    if((xy1[0] == xy3[0]) && (xy1[1] == xy3[1]) && (z1 == z3)) {
        dupvert = 1;
        which_unique = 2;
        dupvalues[0] = xy1[0];
        dupvalues[1] = xy1[1];
        dupvalues[2] = z1;
    }

    if(dupvert)
        printf("duplicate vertex (%d, %d, %d). %d was unique - n1:%d i1:%d n2:%d i2:%d\n", dupvalues[0], dupvalues[1], dupvalues[2], which_unique, n1, i1, n2, i2);

    triangle[0][0] = xy1[0];
    triangle[0][1] = xy1[1];
    triangle[0][2] = z1;

    triangle[1][0] = xy2[0];
    triangle[1][1] = xy2[1];
    triangle[1][2] = z2;

    triangle[2][0] = xy3[0];
    triangle[2][1] = xy3[1];
    triangle[2][2] = z3;



}

int getDist(int a[2], int b[2]) {
    // note: this function returns distance squared, but that's ok for our comparison
    int dx = a[0] - b[0];
    int dy = a[1] - b[1];
    return dx*dx + dy*dy;
}

int getDist3d(int a[2], int b[2]) {
    // note: this function returns distance squared, but that's ok for our comparison
    int dx = a[0] - b[0];
    int dy = a[1] - b[1];
    return dx*dx + dy*dy;
}

