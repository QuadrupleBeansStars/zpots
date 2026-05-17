import { NextRequest, NextResponse } from 'next/server';

const TARGET = process.env.NEXT_API_TARGET ?? 'http://localhost:8000';

async function proxy(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  const url = `${TARGET}/${path.join('/')}${req.nextUrl.search}`;

  const body = ['GET', 'HEAD'].includes(req.method) ? undefined : await req.text();

  const headers = new Headers(req.headers);
  headers.delete('host');
  headers.delete('connection');

  try {
    const upstream = await fetch(url, {
      method: req.method,
      headers,
      body,
    });
    const responseBody = await upstream.text();
    return new NextResponse(responseBody, {
      status: upstream.status,
      headers: { 'content-type': upstream.headers.get('content-type') ?? 'application/json' },
    });
  } catch (err) {
    return NextResponse.json(
      { error: 'API unreachable', detail: String(err) },
      { status: 502 },
    );
  }
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
