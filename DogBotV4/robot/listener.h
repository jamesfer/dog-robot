#pragma once

template <class T, class P>
class Listener {
  typedef void (*ListenerFunction)(P payload);

private:
  T object;
  ListenerFunction listenerFunction;

public:
  Listener(T object, ListenerFunction listener);

  void operator()(P payload);
};

