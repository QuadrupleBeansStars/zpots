import type {
  ChatOwnerRequest, ChatOwnerResponse,
  ChatPlayerRequest, ChatPlayerResponse,
} from './chat-types';

async function postJson<TReq, TRes>(path: string, body: TReq): Promise<TRes> {
  const res = await fetch(`/api/${path}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST /api/${path} failed: ${res.status}`);
  return res.json();
}

export const chatPlayer = (req: ChatPlayerRequest) =>
  postJson<ChatPlayerRequest, ChatPlayerResponse>('chat/player', req);

export const chatOwner = (req: ChatOwnerRequest) =>
  postJson<ChatOwnerRequest, ChatOwnerResponse>('chat/owner', req);
