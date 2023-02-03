import type { HandleFetch } from '@sveltejs/kit';
 
export const handleFetch = (({ request, fetch }) => {
  if (request.url.startsWith('https://api.yourapp.com/')) {
    // clone the original request, but change the URL
    request = new Request(
      request.url.replace('https://api.yourapp.com/', 'http://localhost:9999/'),
      request
    );
  }
 
  return fetch(request);
}) satisfies HandleFetch;