#include <iostream>
#include <cstdlib>
#include <cstdio>
#include <list>
#include <vector>
#include <algorithm>

// Поиск мостов в графе. Мостом является ребро, при удалении которого граф распадается на 2 компоненты связности

// Класс ребра
class Edge
{
public:
	Edge(int a = 0, int b = 0, int _num = 0) : first(a), second(b), num(_num)
	{
	}

	bool operator ==(const Edge& e) const
	{
		return (first == e.first) && (second == e.second);
	}

	int GetFirst() const
	{
		return first;
	}

	int GetSecond() const
	{
		return second;
	}

	int GetNum() const
	{
		return num;
	}

private:
	int first;
	int second;
	int num;
};

// Класс граф, представленный списком смежности
class Graph
{
public:	

	Graph (const  int num_vertices = 0): a(num_vertices)
	{
	}

	void AddEdge(const int k, const int l, const int i)
	{
		Edge e1 (k-1, l-1, i);
		Edge e2 (l-1, k-1, i);
		a[k-1].push_back(e1);
		a[l-1].push_back(e2);
	}

	int GetVertexNum() const
	{
		return a.size();
	}

	const std::vector<Edge>& GetAdjust(const int v) const
	{ 
		return a[v];
	}

	// Проверка на кратные ребра
	bool IsMono (const Edge &e) const
	{
		int num = 0;
		for (size_t i = 0; i < a[e.GetFirst()].size(); i++)
			if (e.GetSecond() == a[e.GetFirst()][i].GetSecond())
			{
				num++;
				if (num > 1)
					return false;
			}
		return true;
	}

private:
	std::vector<std::vector <Edge> > a;
};

// Алгроитм поиска мостов
class BridgesFinder
{
public:
	BridgesFinder (Graph &_g): g(_g), time(1), used(_g.GetVertexNum()), d(_g.GetVertexNum()), low(_g.GetVertexNum())
	{
		for (int i = 0; i < g.GetVertexNum(); i++)
			if (used[i] == false)
				Dfs(i, -1);
	}

	// Модифицированный поиск в глубину, который ищет мосты
	void Dfs(const int v, const int parent)
	{
		used[v] = true;
		d[v] = time;
		low[v] = time++;
		const std::vector<Edge>& adj = g.GetAdjust(v);
		for (size_t i = 0; i < adj.size(); i++)
		{
			int k = adj[i].GetSecond();
			if (k == parent)
				continue;
			if (used[k] == true)
				low[v] = std::min(low[v],d[k]);
			else
			{
				Dfs(k,v);
				low[v] = std::min(low[v], low[k]);
				if (low[k] > d[v])
				{
					if ( g.IsMono(adj[i]) )
						bridge.push_back( adj[i].GetNum() );
				}
			}
		}
	}

	std::vector<int> GetBridges()
	{
		return bridge;
	}

private:
	Graph g;
	std::vector<bool> used;
	std::vector<int> d;
	std::vector<int> low;
	std::vector<int> bridge;
	int time;
};

// Чтение графа
void EdgesIn(Graph &g)
{
	int num_vertex, num_edges;
	scanf ("%d %d", &num_vertex, &num_edges);
	g = Graph(num_vertex);
	for(int i = 1; i <= num_edges ; i++)
	{
		int k,l;
		scanf ("%d %d", &k, &l);
		g.AddEdge(k, l, i);
	}
}

// Вывод списка мостов
void BridgesOut(std::vector<int> bridges)
{
	sort(bridges.begin(), bridges.end());
	printf("%d\n",bridges.size());
	for(size_t i = 0; i < bridges.size(); i++)
		printf("%d\n", bridges[i]);
}

int main()
{
	freopen("bridges.in", "r", stdin);
	freopen("bridges.out", "w", stdout);
	Graph g;
	EdgesIn (g);
	BridgesFinder al (g);
	std::vector<int> bridges = al.GetBridges();
	BridgesOut (bridges);
	return 0;
}