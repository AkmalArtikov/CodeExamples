#include <iostream>
#include <cstdlib>
#include <vector>
#include <string>
#include <exception>
#include <algorithm>
#include <time.h>

// Реализация абстрактного типа данных - очередь с приоритетом. Написана реализация Binary_Heap

// Класс, который будет лежать в узле кучи
template <class T, class U>
class Data {
public:
	Data() : key(), value() {
	}

	Data(const T &_key) : key(_key), value() {
	}

	Data(const T &_key, const U &_value) : key(_key), value(_value) {
	}

	const T& get_key() const {
		return key;
	}

	const U& get_value() const {
		return value;
	}

	bool operator>(const Data<T, U> &rhs) {
		return key > rhs.key;
	}

	bool operator<(const Data<T, U> &rhs) {
		return key < rhs.key;
	}

	bool operator==(const Data<T, U> &rhs) {
		return key == rhs.key;
	}

private:
	T key;
	U value;
};

// Бинарная куча
template <class T>
class BinaryHeap {
public:
	// Исключение, которое будет бросаться при попытке вытащить элемент из пустой кучи
	class EmptyQueue : public std::exception {
	public:
		virtual const char* what() const throw() {
			return "Queue is empty";
		}
	};

	BinaryHeap() : heap_size(0) {
	}

	// Построение кучи по массиву
	BinaryHeap(const std::vector<T> &array) : heap_size(array.size()), heap(array) {
		for (size_t i = heap_size / 2; i >= 0; i--) {
			heapify(i);
		}
	}

	// Добавление нового элемента
	void add(const T &value) {
		heap.push_back(value);
		
		int current = heap_size;
		int parent = (current - 1) / 2;
		
		while (current > 0 && heap[parent] < heap[current]) {
			std::swap(heap[current], heap[parent]);
			current = parent;
			parent = (current - 1) / 2;
		}
		heap_size++;
	}

	// Удаление элеемента с наибольшим приоритетом
	void pop() {
		if (empty()) {
			throw EmptyQueue();
		}

		heap[0] = heap[heap_size - 1];
		heap.pop_back();
		heap_size--;
		heapify(0);
	}


	// сортировка массива с помощью кучи
	std::vector<T> sort(const std::vector<T> &array) const {
		BinaryHeap sorting_heap(array);
		std::vector<T> sorted;

		while (!sorting_heap.empty()) {
			T max = sorting_heap.top();
			sorting_heap.pop();
			sorted.push_back(max);
		}

		return sorted;
	}

	// возвращает элемент с наибольшим приоритетом
	const T& top() const {
		if (empty()) {
			throw EmptyQueue();
		}
		
		return heap[0];
	}

	// возвращает размер кучи
	int size() const {
		return heap_size;
	}

	// Проверка кучи на пустоту 
	bool empty() const {
		return heap_size == 0;
	}

private:
	// Перестройка кучи
	void heapify(size_t index) {
		if (heap_size == 0) {
			return;
		}
		
		size_t left = 2 * index + 1;
		size_t right = 2 * index + 2;
		size_t largest = index;
		
		if (left < heap_size && heap[left] > heap[index]) {
			largest = left;
		}
		if (right < heap_size && heap[right] > heap[largest]) {
			largest = right;
		}
		
		if (largest == index) {
			return;
		}
		else {
			std::swap(heap[index], heap[largest]);
			heapify(largest);
		}
	}

	std::vector<T> heap;
	size_t heap_size;
};


// Случайные тесты
bool RandomTests(size_t size) {
	BinaryHeap<Data<int, std::string> > heap;
	bool is_correct = true;
	srand(time(NULL));

	if (size < 1) {
		size = 10;
	}

	try {
		std::cout << std::endl << "Adding elements" << std::endl << std::endl;

		for (size_t i = 0; i < size; ++i) {
			int key = rand() % 1000;
			std::string value = "Hello!";
			Data<int, std::string> node(key, value);
			heap.add(node);
			std::cout << key << " " << value << " added" << std::endl;
		}
	
		std::cout << std::endl << "Popping elements" << std::endl << std::endl;

		Data<int, std::string> node = heap.top();
		heap.pop();
		std::cout << node.get_key() << " " << node.get_value() << " popped" << std::endl;

		for (size_t i = 0; i < size / 2; ++i) {
			Data<int, std::string> cur_node = heap.top();
			heap.pop();
			if (node.get_key() < cur_node.get_key()) {
				is_correct = false;
				return is_correct;
			}
			node = cur_node;
			std::cout << node.get_key() << " " << node.get_value() << " popped" << std::endl;
		}

		std::cout << std::endl << "Adding elements again" << std::endl << std::endl;

		for (size_t i = 0; i < size; ++i) {
			int key = rand() % 1000;
			std::string value = "Hello!";
			Data<int, std::string> node(key, value);
			heap.add(node);
			std::cout << key << " " << value << " added" << std::endl;
		}

		std::cout << std::endl << "Popping elements again" << std::endl << std::endl;

		node = heap.top();
		heap.pop();
		std::cout << node.get_key() << " " << node.get_value() << " popped" << std::endl;

		while (!heap.empty()) {
			Data<int, std::string> cur_node = heap.top();
			heap.pop();
			if (node.get_key() < cur_node.get_key()) {
				is_correct = false;
				return is_correct;
			}
			node = cur_node;
			std::cout << node.get_key() << " " << node.get_value() << " popped" << std::endl;
		}
	}
	catch (const std::exception& e) {
		std::cerr << "EXCEPTION: " << e.what() << std::endl;
		is_correct = false;
	}
	
	return is_correct;
}

int main(int argc, char **argv) {
	size_t size;

	if (argc == 2) {
		size = atoi(argv[1]);
	}
	else {
		std::cout << "Input the size of test" << std::endl;
		std::cin >> size;
	}

	if (RandomTests(size)) {
		std::cout << std::endl <<"Everything is OK" << std::endl;
	} 
	else {
		std::cout << std::endl << "Error is detected" << std::endl;
	}

	return 0;
}


