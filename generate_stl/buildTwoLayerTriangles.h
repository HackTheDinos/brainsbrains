#ifndef GENSTL_BUILDTRI
#define GENSTL_BUILDTRI

void generateTriangles(int triangles[][3][3], int l1[][2], int n1, int z1, int l2[][2], int n2, int z2);
void addTriangle(int n1, int i1, int n2, int i2, int triangle[][3], int xy1[2], int z1, int xy2[2], int z2, int xy3[2], int z3);
int getDist(int a[2], int b[2]);

#endif
