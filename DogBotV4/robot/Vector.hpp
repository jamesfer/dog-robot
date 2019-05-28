#pragma once

#include "Arduino.h"
#include "Swap.hpp"

template <class T>
class Vector
{
protected:
	int size;
	int capacity;
	T* data = nullptr;

public:
	Vector() : data(nullptr), size(0), capacity(0) {}

	Vector(int cap) : Vector()
	{
		reserve(cap);
	}

	Vector(const T* input, int inputSize) : Vector(inputSize)
	{
//		std::memcpy(data, input, sizeof(T) * inputSize);
		while (size < inputSize)
		{
			append(input[size]);
		}
	}

	Vector(const Vector& other) : Vector(other.data, other.size)
	{

	}

	virtual ~Vector()
	{
		if (data) {
			delete [] data;
		}
	}

	friend void swap(Vector& first, Vector& second)
	{
		swap(first.size, second.size);
		swap(first.capacity, second.capacity);
		swap(first.data, second.data);
	}

	Vector& operator=(Vector other)
	{
		swap(*this, other);
		return *this;
	}

	T operator[](unsigned int i) const
	{
		return data[i];
	}

	T& operator[](unsigned int i)
	{
		return data[i];
	}

	bool operator==(const Vector<T>& other) const
	{
		if (size != other.size)
		{
			return false;
		}

		for (int i = 0; i < size; i++)
		{
			if (data[i] != other[i])
			{
				return false;
			}
		}

		return true;
	}

	bool operator!=(const Vector<T>& other) const
	{
		return !operator==(other);
	}

	void append(const T& item)
	{
		reserve(size + 1);
		setSize(size + 1);
		data[size - 1] = item;
	}

	virtual void reserve(int newCap)
	{
		if (newCap <= capacity)
		{
			return;
		}

		if (newCap != 0)
		{
			// Copy old data into new data block
			T* newData = new T[newCap];
			if (data != nullptr)
			{
				for (int i = 0; i < size; i++)
				{
					newData[i] = data[i];
				}
				delete [] data;
			}
			data = newData;
			capacity = newCap;
		}
	}

//	void resize(int newCap)
//	{
//		if (newCap == capacity)
//		{
//			return;
//		}
//
//		int newSize = size > newCap ? newCap : size;
//		if (newCap != 0)
//		{
//			T* newData = new T[newCap];
//
//			if (data != nullptr)
//			{
//				for (int i = 0; i < newSize; i++)
//				{
//					newData[i] = data[i];
//				}
//				delete[] data;
//			}
//
//			data = newData;
//		}
//		else
//		{
//			data = nullptr;
//		}
//
//		capacity = newCap;
//		setSize(newSize);
//	}

	void clear()
	{
		setSize(0);
	}

	inline const T* getData() const { return data; }
	inline int getSize() const { return size; }
	inline int getCapacity() const { return capacity; }

protected:
	/**
	 * Increases the capacity of the vector to be at least minCapacity items long.
	 * Does nothing if the array is already that size.
	 * @param minCapacity New minimum capacity
	 */
//	void reserveMinimumCapacity(int minCapacity)
//	{
//		if (minCapacity > capacity)
//		{
//			int newCapacity = capacity == 0 ? 1 : capacity;
//			while (newCapacity < minCapacity)
//			{
//				newCapacity *= 2;
//			}
//			resize(newCapacity);
//		}
//	}

	virtual void setSize(int newSize)
	{
		size = newSize;
	}
};
