# Vercel Frontend Deployment

The FlowState web UI is hosted outside this repository. This repo exposes only the FlowState backend API origin.

## Required API Origin

Set the frontend's API origin to the HTTPS reverse-proxy origin from the VPS:

```text
https://api.example.com
```

Use no trailing slash.

For the FlowState Vite/Vue web build, use this environment variable in Vercel:

```text
VITE_FLOWSTATE_API_ORIGIN=https://api.example.com
```

If the upstream FlowState web UI still assumes same-origin `/api` calls, keep the same API origin and add a Vercel rewrite in that frontend project instead:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.example.com/api/:path*"
    }
  ]
}
```

## Backend Settings Required For Vercel

On the VPS, set the FlowState auth/CORS origin list to include every Vercel production and preview URL that should be allowed:

```text
FLOWSTATE_AUTH_SECURE_COOKIES=true
FLOWSTATE_AUTH_ALLOWED_ORIGINS=https://your-project.vercel.app,https://www.example.com
```

Restart FlowState after changing `/etc/fullspektrum/flowstate.env`:

```bash
sudo systemctl restart flowstate
```

## Deployment Boundary

Do not build or serve the FlowState web UI from this repo. The Vercel project should point at the FlowState web source and only needs the API origin above to reach this backend deployment.
