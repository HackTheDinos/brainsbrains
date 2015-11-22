void addTriangle(int triangle[][3], int xy1[2], int z1, int xy2[2], int z2, int xy3[2], int z3);
int getDist(int a[2], int b[2]);

void generateTriangles(int triangles[][3][3], int l1[][2], int n1, int z1, int l2[][2], int n2, int z2) {
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
               addTriangle(triangles[i1+i2], l1[i1], z1, l2[i2], z2, l2[i2+1], z2);
               i2++;
            } else {
               addTriangle(triangles[i1+i2], l1[i1], z1, l2[i2], z2, l1[i1+1], z1);
               i1++;
            }
        } else if(i2<n2-1) {
           addTriangle(triangles[i1+i2], l1[i1], z1, l2[i2], z2, l2[i2+1], z2);
           i2++;
        } else if(i1<n1-1) {
           addTriangle(triangles[i1+i2], l1[i1], z1, l2[i2], z2, l1[i1+1], z1);
           i1++;
        } else {
            int d12 = getDist(l1[i1], l2[0]);
            int d21 = getDist(l2[i2], l1[0]);

            if(d12 < d21) {
               addTriangle(triangles[i1+i2], l1[i1], z1, l2[i2], z2, l2[0], z2);
               addTriangle(triangles[i1+i2+1], l1[i1], z1, l2[0], z2, l1[0], z1);
            } else {
               addTriangle(triangles[i1+i2], l1[i1], z1, l2[i2], z2, l1[0], z1);
               addTriangle(triangles[i1+i2+1], l1[0], z1, l2[i2], z2, l2[0], z2);
            }
            done = 1;
        }
    }
}

void addTriangle(int triangle[][3], int xy1[2], int z1, int xy2[2], int z2, int xy3[2], int z3) {
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
