# @wos/dummy

A demonstration package showing how to create and structure WOS (Wings Operating System) packages.

## Overview

This is a dummy package created to showcase the structure and configuration of a WOS package. It implements a typical user and post service system commonly found in social applications.

## Features

- **User Service**: Complete user management system with CRUD operations

  - User creation, retrieval, updates, and deletion
  - Authentication functionality
  - User status management

- **Post Service**: Social posting system with CRUD operations
  - Post creation, retrieval, updates, and deletion
  - Comment functionality
  - Like/unlike functionality
  - Post visibility control

## Components

This package contains three main nodes:

1. **run_user**: Launches the user service
2. **run_post**: Launches the post service
3. **run_server**: Main server that depends on both services

## Configuration

You can configure this package using the following parameters:

- **port**: The port on which the services will run (default: 8080)
- **dev_mode**: Boolean indicating whether to run in development mode (default: false)

## Development

To run this package in development mode:

```bash
wos run @wos/dummy --dev
```

This will use the development settings (port 9090 and dev_mode=true).

## Package Structure

```
@wos/dummy/
├── proto/
│   ├── service_config.proto
│   ├── user_service.proto
│   └── post_service.proto
├── run-user.py
├── run-post.py
├── run-server.py
├── README.md
├── LICENSE
└── wos.yml
```

## Usage Example

This is a demonstration package only and is not intended for production use. It serves as a reference for WOS package structure and configuration.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
