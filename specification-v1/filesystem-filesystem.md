# Filesystem

## Overview
The Filesystem interface is intended for local filesystem operations on a resource.  These are relatively fine-grained local operations.  This interface is not intended for inter-resource and inter-facility transfers, but is intended for local workflow file management expecially run artifacts, for example applicaiton output and error streams.  All operations are asynchronus and status may be checked via the task API endpoints.  Any of these may be implemented by a compliant implementation.  If an API method is not supported a `501: Not Implemented` error must be returned.

## Attributes

### PutFileChmodRequest
A `PutFileChmodRequest` is defined with the following attributes:

| Attribute       | Type  | Description  | Required | Example |
|-----------------|-------|--------------|----------|---------|
| `mode` | string | String specifying the file mode bits to set. | Yes | `0750` |
| `path` | string | Path of file on resrouce to modify. | Yes | `/scratch/myproject/foo.txt` | 


### PutFileChownRequest
A `PutFileChownRequest` is defined with the following attributes:

| Attribute       | Type  | Description  | Required | Example |
|-----------------|-------|--------------|----------|---------|
| `group` | string | Group to change.  If omitted group will not be changed | No |  `my-group`|
| `owner` | string | User to change ownsership to. | No | `user` |
| `path` | string | Path of file on resrouce to modify. | Yes | `/home/user/dir/file.out` |

### PostMakeDirRequest
A `PostMakeDirRequest` is defined with the following attributes:

| Attribute       | Type  | Description  | Required | Example |
|-----------------|-------|--------------|----------|---------|
| `parent`| boolean | Make parent directories if they do not exist on the `path`. | Yes | `true` |
| `path`| string | Path of directory to create. | Yes | `/home/user/dir/newdir` |

### PostFileSymlinkRequest
A `PostFileSymlinkRequest` is defined with the following attributes:

| Attribute       | Type  | Description  | Required | Example |
|-----------------|-------|--------------|----------|---------|
| `link_path`| string | Path of symbolic link. | Yes | `/home/user/newlink`|
| `path` | string | Path of symbolic link target. | Yes |`/home/user/dir`|

### PostCompressRequest
A `PostCompressRequest` is defined with the following attributes:

Compression types include `none`, `bzip2`, `gzip`, `xz`

| Attribute       | Type  | Description  | Required | Example |
|-----------------|-------|--------------|----------|---------|
| `compression`| string | Compression scheme to use. `gzip` is used by default. | No | `none` |
| `dereference`| string | Follow symbolic links and archive and dump the files they point to if true. | No | `true` | 
| `matchPattern`| string | Regex pattern to match for files to compress. | No | `*./[ab].*\\.txt` | 
| `sourcePath`| string | Path to directory to compress. | Yes | `/home/user/dir` |
| `targetPath`| string | Path of compressed output. | Yes | `/home/user/file.tar.gz` |

### PostExtractRequest
A `PostExtractRequest` is defined with the following attributes:

Compression types include `none`, `bzip2`, `gzip`, `xz`

| Attribute       | Type  | Description  | Required | Example |
|-----------------|-------|--------------|----------|---------|
| `compression` | string | Compression that is used with the file. Default is `gzip`. | No | `none` |
| `sourcePath`  | string | File to decompress. | Yes | `/home/user/dir/file.tar.gz` |
| `targetPath`  | string | Path to the directory where to extract the compressed file | Yes|  `/home/user/dir` | 

### PostMoveRequest
A `PostMoveRequest` is defined with the following attributes:

| Attribute       | Type  | Description  | Required | Example |
|-----------------|-------|--------------|----------|---------|
| `sourcePath` | string | Source of file to move. | Yes | `/home/user/dir/file.orig` |
| `targetPath` | string | Target path of the move operation. | Yes | `/home/user/dir/file.new` |

### PostCopyRequest
A `PostCopyRequest` is defined with the following attributes:

| Attribute       | Type  | Description  | Required | Example |
|-----------------|-------|--------------|----------|---------|
| `sourcePath` | string | Source of file to copy. | Yes | `/home/user/dir/file.orig` |
| `targetPath` | string | Target path of the copy operation. | Yes | `/home/user/dir/file.new` |
| `dereference`| string | Follow symbolic links and copy the files they point to instead of the link if set to `true`. | No | `true` | 

## API Endpoints

### PUT `/filesystem/chmod/{resource_id}`
Request to change file permissions on a resource with `resource_id`. Return
a `task_id` that can be queried for the status and completion of the operation.
Parameters to `chmod` are specified in a `PutFileChmodRequest` object.

**Parameters**: 
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource. |

**Body**:
`PutFileChmodRequest`

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/chmod/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/chmod/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/chmod/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/chmod/abc123"
}
```

### PUT `/filesystem/chown/{resource_id}`
A request to run `chown` on a file on a resource specified by `resource_id`.
Parameters to `chown` are specified in a `PutFileChownRequest` object.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|

**Body**:
`PutFileChownRequest`

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesytsem/chown/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/chown/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/chown/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/chmod/abc123"
}
```

### GET `/filesystem/file/{resource_id}`
Output the type of a file or directory on the resource specified by `resource_id`.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|
| `path`| string | N/A | a file or folder path. |

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/file/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/file/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/file/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/file/abc123"
}
```

### GET `/filesystem/stat/{resource_id}`
Output the `stat` of a file.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|
| `path`| string | N/A | a file or folder path. |

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/stat/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/stat/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/stat/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/stat/abc123"
}
```

### POST `/filesystem/mkdir/{resource_id}`
Create directory specified by a `PostMakeDirRequest` on resource `resource_id`.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|

**Body**:
`PostMakeDirRequest`

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesytsem/mkdir/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/mkdir/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/mkdir/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/mkdir/abc123"
}
```

### POST `/filesystem/symlink/{resource_id}`
Create symlink specified by a `PostFileSymlinkRequest` on resource `resource_id`.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|

**Body**:
`PostFileSymlinkequest`

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesytsem/symlink/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/symlink/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/mksymlink/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/symlink/abc123"
}
```

### GET `/filesystem/ls/{resource_id}`
List files specified in `path` on `resource_id`.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|
| `path`| string | N/A | a file or folder path. |
| `showHidden` | boolean | `false`| Show hidden files if `true`.|
| `numericUid` | boolean | `false` | Show numeric user and group ids if `true`. |
| `recursive` | boolean | `false`| recursively list files and folders if `true`. |
| `dereference` | boolean | `false`| Show information for the file symlinks reference if `true`. |

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/ls/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/ls/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/ls/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/ls/abc123"
}
```

### GET `/filesystem/head/{resource_id}`
Output the firt part of the file specified at `path`.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|
| `path`| string | N/A | a file or folder path. |
| `bytes` | integer | N/A| Output the first NUM bytes of each file.|
| `lines` | boolean | N/A | Show numeric user and group ids if `true`. |
| `skipTrailing` | boolean | `false`| The output will be the whole file withouth the last NUM bytes/lines of each file.  Numb should be specified thorugh `bytes` or `lines` if `true`. |

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/head/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/head/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/head/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/head/abc123"
}
```

### GET `/filesystem/view/{resource_id}`
View file content at `path`.  Maximum bytes returned is site-dependent.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource. |
| `path`| string | N/A | a file or folder path. |
| `size` | integer | site maximum | The size of data to be retrieved from the file in bytes. |
| `offset` | integer | 0 | Offset to start from in file in bytes. |


**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/view/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/view/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/view/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/view/abc123"
}
```

### GET `/filesystem/tail/{resource_id}`
Output the last part of the file specified at `path`.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|
| `path`| string | N/A | a file or folder path. |
| `bytes` | integer | N/A| Output the first NUM bytes of each file.|
| `lines` | boolean | N/A | Show numeric user and group ids if `true`. |
| `skipHeading` | boolean | `false`| The output will be the whole file withouth the first NUM bytes/lines of each file.  Numb should be specified thorugh `bytes` or `lines` if `true`. |

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/tail/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/tail/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/tail/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/tail/abc123"
}
```

### GET `/filesystem/checksum/{resource_id}`
Output the checksum of a file at `path` using the SHA-256 algorithm.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|
| `path`| string | N/A | a file or folder path. |

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/checksum/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/checksum/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/checksum/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/checksum/abc123"
}
```
 
### DELETE `/filesystem/rm/{resource_id}`
Delete file or directory at `path`.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|
| `path`| string | N/A | a file or folder path. |


**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/rm/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/rm/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/rm/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/rm/abc123"
}
```

### POST `/filesystem/compress/{resource_id}`
Compress the files and directories specified in the `PostCompressRequest` object with the `tar` command.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|

**Body**:
`PostCompressRequest`

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/compress/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/compress/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/compress/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/compress/abc123"
}
```

 
### POST `/filesystem/extract/{resource_id}`
Extract the files and directories specified in the `PostExtractRequest` object with the `tar` command.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|

**Body**:
`PostExtractRequest`

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/extract/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/extract/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/extract/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/extract/abc123"
}
```

### POST `/filesystem/mv/{resource_id}`
Move a file specified by the `PostMoveRequest` object.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|

**Body**:
`PostMoveRequest`

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/mv/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/mv/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/mv/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/mv/abc123"
}
```
 
### POST `/filesystem/cp/{resource_id}`
Copy a file as specified by the `PostCopyRequest` object.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource.|

**Body**:
`PostCopyRequest`

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/cp/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/cp/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/cp/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/cp/abc123"
}
```

 
### GET `/filesystem/download/{resource_id}`
Download a small file from `path`.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource. |
| `path` | string | N/A | Download a file located at `path`. | 

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/download/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/download/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/download/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/download/abc123"
}
```
 
### POST `/filesystem/upload/{resource_id}`
Upload a small file to `path` on the resource specified by `resource_id`.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_id` | string | N/A | `resource_id` of target resource. |
| `path` | string | N/A | Upload a file located at `path`. | 

**Responses**:

**Succesful Repsonse**
- Code: 200
- Media Type: application/json

Example Response:
```json
"123456"
```

**Unauthorized**
- Code 401
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/filesystem/upload/abc123"
}
```
**Forbidden**
- Code: 403
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/filesystem/upload/abc123"
}
```

**Not Found**
- Code: 404
- Media Type: applicaiton/problem+json
```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The resource ID 'abc123' does not exist.",
  "instance": "/api/v1/filesystem/upload/abc123"
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/problem+json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/filesystem/upload/abc123"
}
```

### GET `/task/{task_id}`
Get an outstanding task with an id of `task_id`.

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `task_id` | string | N/A | The `task_id` of the task status and result to retrieve. |

**Responses**:

**Successful Repsonse**
- Code: 200
- Media type: applicaiton/json
 
 ```json
{
  "id": "12345",
  "status": "string",
  "result": "string",
  "command": {
    "router": "string",
    "command": "string",
    "args": {
      "additionalProp1": {}
    }
  }
}
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/json
```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/task"
}
```


### GET `/task`
Get all outstanding tasks.  This takes no parameters.

**Parameters**:
None

**Responses**:

**Successful Repsonse**
- Code: 200
- Media type: applicaiton/json
 ```json
[
  {
    "id": "string",
    "status": "string",
    "result": "string",
    "command": {
      "router": "string",
      "command": "string",
      "args": {
        "additionalProp1": {}
      }
    }
  }
]
```

**Internal Server Error**
- Code: 500
- Media Type: applicaiton/json

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/task"
}
```