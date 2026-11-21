// tarjan_ref.cpp - Implementacion de REFERENCIA (solo para probar la Parte B).
// La version oficial del proyecto es la de la Parte A; debe respetar el mismo contrato de traza.
#include <bits/stdc++.h>
using namespace std;

int n, m, timer_ = 0;
vector<pair<int,int>> E;
vector<vector<pair<int,int>>> adj;
vector<int> tin, low;
vector<char> isBridge;
long long ops = 0;
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

void dfs(int u, int parentEdge) {
    tin[u] = low[u] = timer_++; ops++;
    ev("{\"t\":\"enter\",\"v\":%d,\"tin\":%d,\"ops\":%lld}", u, tin[u], ops);
    for (auto [v, id] : adj[u]) {
        ops++;
        if (id == parentEdge) continue;              // se salta por ID de arista (soporta paralelas)
        if (tin[v] != -1) {
            if (tin[v] < tin[u]) {                   // back edge hacia un ancestro
                low[u] = min(low[u], tin[v]);
                ev("{\"t\":\"back\",\"u\":%d,\"v\":%d,\"e\":%d,\"low\":%d,\"ops\":%lld}", u, v, id, low[u], ops);
            }
            continue;                                // (si tin[v] > tin[u], es el otro extremo de una back edge ya vista)
        }
        ev("{\"t\":\"tree\",\"u\":%d,\"v\":%d,\"e\":%d,\"ops\":%lld}", u, v, id, ops);
        dfs(v, id);
        low[u] = min(low[u], low[v]);
        ev("{\"t\":\"low\",\"v\":%d,\"low\":%d,\"ops\":%lld}", u, low[u], ops);
        bool br = low[v] > tin[u];                   // criterio de puente
        if (br) isBridge[id] = 1;
        ev("{\"t\":\"check\",\"u\":%d,\"v\":%d,\"e\":%d,\"lowv\":%d,\"tinu\":%d,\"bridge\":%s,\"ops\":%lld}",
           u, v, id, low[v], tin[u], br ? "true" : "false", ops);
    }
    ev("{\"t\":\"exit\",\"v\":%d,\"ops\":%lld}", u, ops);
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
    tin.assign(n, -1); low.assign(n, -1); isBridge.assign(m, 0);
    for (int s = 0; s < n; s++)
        if (tin[s] == -1) {                           // grafo desconectado: un DFS por componente
            ev("{\"t\":\"new_root\",\"v\":%d,\"ops\":%lld}", s, ops);
            dfs(s, -1);
        }
    printf("{\n  \"algo\": \"tarjan\",\n  \"n\": %d,\n  \"edges\": [", n);
    for (int i = 0; i < m; i++) printf("%s[%d,%d]", i ? "," : "", E[i].first, E[i].second);
    printf("],\n  \"bridges\": [");
    bool f = true;
    for (int i = 0; i < m; i++) if (isBridge[i]) { printf("%s%d", f ? "" : ",", i); f = false; }
    printf("],\n  \"ops\": %lld,\n  \"events\": [%s\n  ]\n}\n", ops, out.c_str());
}
