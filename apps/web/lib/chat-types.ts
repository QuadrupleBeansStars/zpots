// Mirrors apps/api/schemas/chat.py

export type ChatRole = 'user' | 'assistant' | 'tool' | 'system';

export type ChatToolCall = {
  id: string;
  type: 'function';
  function: { name: string; arguments: string };
};

export type ChatMessage = {
  role: ChatRole;
  content?: string | null;
  tool_calls?: ChatToolCall[] | null;
  tool_call_id?: string | null;
};

export type ChatUser = { id: number; name: string };

export type BookingSnapshot = {
  txn_id: string;
  court_id: string;
  court_name: string;
  date: string;
  time_start: string;
  time_end: string;
  duration: number;
  total_price: number;
  status: 'CONFIRMED' | 'CANCELLED';
};

export type BookingDraft = {
  kind: 'booking_draft';
  court_id: string;
  court_name: string;
  date: string;
  time_start: string;
  time_end: string;
  duration: number;
  total_price: number;
};

export type CancelDraft = {
  kind: 'cancel_draft';
  txn_id: string;
  court_name: string;
  date: string;
  time_start: string;
};

export type ChatDraft = BookingDraft | CancelDraft;

export type ChatPlayerRequest = {
  messages: ChatMessage[];
  user: ChatUser;
  bookings: BookingSnapshot[];
};
export type ChatPlayerResponse = {
  text: string;
  draft: ChatDraft | null;
  history: ChatMessage[];
};

export type ChatOwnerRequest = {
  messages: ChatMessage[];
  user: ChatUser;
};
export type ChatOwnerResponse = {
  text: string;
  history: ChatMessage[];
};
