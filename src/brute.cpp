// brute.cpp - Fuerza bruta para puentes: quita cada arista y prueba conectividad con BFS.
// Entrada (stdin):  n m  y luego m lineas "u v" (vertices 0-indexados, id de arista = indice de linea).
// Salida (stdout):  traza JSON (ver README). Opcion --compact: sin eventos, solo resultado y ops.
// Complejidad: O(E * (V + E)).
#include <bits/stdc++.h>
using namespace std;

int n, m;
vector<pair<int,int>> E;
vector<vector<pair<int,int>>> adj;   // (vecino, id de arista)
long long ops = 0;                   // operaciones elementarias (ver README)
bool compact = false, firstEv = true;
string out;

template <class... A> void ev(const char* f, A... a) {
    if (compact) return;
    char buf[256];
    snprintf(buf, sizeof buf, f, a...);
    if (!firstEv) out += ",";
    firstEv = false;
    out += "\n    "; out += buf;
}

// Cuenta componentes conexas ignorando la arista 'skip' (-1 = ninguna). BFS desde cada nodo no visitado.
int countComponents(int skip, bool emitVisits) {
    vector<char> vis(n, 0);
    int c = 0;
    for (int s = 0; s < n; s++) {
        if (vis[s]) continue;
        c++;
        queue<int> q; q.push(s); vis[s] = 1; ops++;
        if (emitVisits) ev("{\"t\":\"visit\",\"v\":%d,\"ops\":%lld}", s, ops);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto [v, id] : adj[u]) {
                ops++;                         // se examina una entrada de la lista de adyacencia
                if (id == skip) continue;      // arista "eliminada" (por id, no por vertices)
                if (!vis[v]) {
                    vis[v] = 1; q.push(v); ops++;
                    if (emitVisits) ev("{\"t\":\"visit\",\"v\":%d,\"ops\":%lld}", v, ops);
                }
            }
        }
    }
    return c;
}

int main(int argc, char** argv) {
    for (int i = 1; i < argc; i++) if (string(argv[i]) == "--compact") compact = true;
    if (scanf("%d %d", &n, &m) != 2) return 1;
    E.resize(m); adj.assign(n, {});
    for (int i = 0; i < m; i++) {
        if (scanf("%d %d", &E[i].first, &E[i].second) != 2) return 1;
        auto [u, v] = E[i];
        adj[u].push_back({v, i});
        if (u != v) adj[v].push_back({u, i});
    }
    int base = countComponents(-1, false);
    ev("{\"t\":\"start\",\"base\":%d,\"ops\":%lld}", base, ops);
    vector<int> bridges;
    for (int e = 0; e < m; e++) {
        ev("{\"t\":\"remove\",\"e\":%d,\"ops\":%lld}", e, ops);
        int c = countComponents(e, true);
        bool br = c > base;                    // si aumentan las componentes, e es puente
        if (br) bridges.push_back(e);
        ev("{\"t\":\"check\",\"e\":%d,\"comps\":%d,\"base\":%d,\"bridge\":%s,\"ops\":%lld}",
           e, c, base, br ? "true" : "false", ops);
        ev("{\"t\":\"restore\",\"e\":%d,\"ops\":%lld}", e, ops);
    }
    printf("{\n  \"algo\": \"brute\",\n  \"n\": %d,\n  \"edges\": [", n);
    for (int i = 0; i < m; i++) printf("%s[%d,%d]", i ? "," : "", E[i].first, E[i].second);
    printf("],\n  \"bridges\": [");
    for (size_t i = 0; i < bridges.size(); i++) printf("%s%d", i ? "," : "", bridges[i]);
    printf("],\n  \"ops\": %lld,\n  \"events\": [%s\n  ]\n}\n", ops, out.c_str());
}
