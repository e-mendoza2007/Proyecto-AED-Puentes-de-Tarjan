// Parte A - Puentes en un grafo no dirigido con el algoritmo de Tarjan (DFS + tin/low).
// Entrada: "n m" y m lineas "u v" (0-indexado). El id de cada arista es su indice.
// Salida: JSON con los puentes y la traza de eventos que reproduce Manim.
// Uso: bin/tarjan < graphs/demo.txt            (con eventos)
//      bin/tarjan --compact < graphs/demo.txt  (solo resultado y ops)
#include <bits/stdc++.h>
using namespace std;

struct Arista {
    int to, id;
};

int n, m, timer_ = 0;
long long ops = 0;
bool compact = false;
vector<pair<int, int>> aristas;
vector<vector<Arista>> adj;
vector<int> tin, low;
vector<bool> esPuente;
vector<string> eventos;

void evento(string s) {
    if (compact) return;
    eventos.push_back(s);
}

string num(long long x) {
    return to_string(x);
}

void dfs(int u, int aristaPadre) {
    tin[u] = timer_;
    low[u] = timer_;
    timer_++;
    ops++;
    evento("{\"t\":\"enter\",\"v\":" + num(u) + ",\"tin\":" + num(tin[u]) + ",\"ops\":" + num(ops) + "}");

    for (int i = 0; i < (int)adj[u].size(); i++) {
        int v = adj[u][i].to;
        int id = adj[u][i].id;
        ops++;

        if (id == aristaPadre) continue;

        if (tin[v] != -1) {
            if (tin[v] < tin[u]) {
                low[u] = min(low[u], tin[v]);
                evento("{\"t\":\"back\",\"u\":" + num(u) + ",\"v\":" + num(v) + ",\"e\":" + num(id) +
                       ",\"low\":" + num(low[u]) + ",\"ops\":" + num(ops) + "}");
            }
            continue;
        }

        evento("{\"t\":\"tree\",\"u\":" + num(u) + ",\"v\":" + num(v) + ",\"e\":" + num(id) + ",\"ops\":" + num(ops) + "}");
        dfs(v, id);

        low[u] = min(low[u], low[v]);
        evento("{\"t\":\"low\",\"v\":" + num(u) + ",\"low\":" + num(low[u]) + ",\"ops\":" + num(ops) + "}");

        bool puente = low[v] > tin[u];
        if (puente) esPuente[id] = true;
        evento("{\"t\":\"check\",\"u\":" + num(u) + ",\"v\":" + num(v) + ",\"e\":" + num(id) +
               ",\"lowv\":" + num(low[v]) + ",\"tinu\":" + num(tin[u]) +
               ",\"bridge\":" + (puente ? "true" : "false") + ",\"ops\":" + num(ops) + "}");
    }

    evento("{\"t\":\"exit\",\"v\":" + num(u) + ",\"ops\":" + num(ops) + "}");
}

int main(int argc, char** argv) {
    for (int i = 1; i < argc; i++)
        if (string(argv[i]) == "--compact") compact = true;

    if (scanf("%d %d", &n, &m) != 2) return 1;

    adj.resize(n);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (scanf("%d %d", &u, &v) != 2) return 1;
        aristas.push_back({u, v});
        adj[u].push_back({v, i});
        if (u != v) adj[v].push_back({u, i});
    }

    for (int i = 0; i < n; i++) {
        tin.push_back(-1);
        low.push_back(-1);
    }
    for (int i = 0; i < m; i++) esPuente.push_back(false);

    for (int s = 0; s < n; s++) {
        if (tin[s] == -1) {
            evento("{\"t\":\"new_root\",\"v\":" + num(s) + ",\"ops\":" + num(ops) + "}");
            dfs(s, -1);
        }
    }

    printf("{\n  \"algo\": \"tarjan\",\n  \"n\": %d,\n  \"edges\": [", n);
    for (int i = 0; i < m; i++)
        printf("%s[%d,%d]", i ? "," : "", aristas[i].first, aristas[i].second);
    printf("],\n  \"bridges\": [");
    bool primero = true;
    for (int i = 0; i < m; i++) {
        if (esPuente[i]) {
            printf("%s%d", primero ? "" : ",", i);
            primero = false;
        }
    }
    printf("],\n  \"ops\": %lld,\n  \"events\": [", ops);
    for (int i = 0; i < (int)eventos.size(); i++)
        printf("%s\n    %s", i ? "," : "", eventos[i].c_str());
    printf("\n  ]\n}\n");
    return 0;
}
