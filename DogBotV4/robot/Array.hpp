#pragma once

template <class T, int N>
class Array
{
  template<class U, int N2> friend class Array;

public:
  // Data stored in the array.
  T data[N];

  constexpr unsigned int size() const
  {
    return N;
  }

  // Copy Assignment operator.
  Array& operator=(const Array& other)
  {
    memcpy(&data, &other.data, sizeof(T) * N);

    return *this;
  }

  // Subscript operator
  T& operator[](const unsigned int index)
  {
    return data[index];
  }

  // Subscript operator
  const T& operator[](const unsigned int index) const
  {
    return data[index];
  }

  // Concatenation operator
  template <int N2>
  Array<T, N + N2> operator+(const Array<T, N2>& other) const
  {
    Array<T, N + N2> result;

    memcpy(&result.data, &data, sizeof(T) * N);
    memcpy(&(result.data[N]), &other.data, sizeof(T) * N2);

    return result;
  }

  template <class Functor>
  void each(const Functor& functor) const
  {
    for (int i = 0; i < size(); i++)
    {
      functor(data[i]);
    }
  }

  template <class Functor>
  void eachIndex(const Functor& functor) const
  {
    for (int i = 0; i < size(); i++)
    {
      functor(data[i], i);
    }
  }

  template <class R, class Functor>
  R reduce(const Functor& functor, const R& initialValue = {}) const
  {
    if (size() == 0)
    {
      return initialValue;
    }

    R result = functor(initialValue, data[0]);
    for (int i = 1; i < size(); i++)
    {
      result = functor(result, data[i]);
    }

    return result;
  }

  template <class U, class Functor>
  Array<U, N> map(const Functor& functor) const
  {
    Array<U, N> result;
    for (int i = 0; i < size(); i++)
    {
      result[i] = functor(data[i]);
    }

    return result;
  }

  Array<Array<T, 2>, N> zip(const Array<T, N>& b) const
  {
    Array<Array<T, 2>, N> result;
    for (int i = 0; i < N; i++)
    {
      result[i] = {data[i], b[i]};
    }

    return result;
  }

  template <class Functor>
  T* find(const Functor& functor)
  {
    for (int i = 0; i < size(); i++)
    {
      if (functor(data[i]))
      {
        return &data[i];
      }
    }
    return nullptr;
  }
};
