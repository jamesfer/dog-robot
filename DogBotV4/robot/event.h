#pragma once

template <class P, int L>
class Event {
  typedef void (*ListenerFunction)(P payload);

private:
  ListenerFunction listeners[L];
  unsigned int listenerCount;

public:
  void fire(P payload);

  void listen(ListenerFunction listener);
};
