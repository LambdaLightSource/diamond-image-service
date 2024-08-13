function read_file(path)
    local file, errorMessage = io.open(path, "rb")
    if not file then
        error("Could not read the file: " .. errorMessage .. "\n")
    end

    local content = file:read("*all")
    file:close()
    return content
end

-- Unique boundary string similar to what curl might generate
local Boundary = "----WebKitFormBoundary" .. tostring(os.time())
local BodyBoundary = "--" .. Boundary
local LastBoundary = "--" .. Boundary .. "--"
local CRLF = "\r\n"

-- Function to prepare the multipart/form-data body
function prepare_multipart_data(file_path)
    local file_content = read_file(file_path)
    local filename = file_path:match("^.+/(.+)$")  -- Extract filename from the path

    local ContentDisposition = 'Content-Disposition: form-data; name="media"; filename="' .. filename .. '"'
    local ContentType = 'Content-Type: image/png'  -- Adjust this to match your file type

    local body = BodyBoundary .. CRLF .. ContentDisposition .. CRLF .. ContentType .. CRLF .. CRLF .. file_content .. CRLF .. LastBoundary

    return body, Boundary
end

-- Generate the HTTP request
function request()
    local image_num = math.random(0, 999)
    local file_path = "generated_images/random_image_" .. string.format("%06d", image_num) .. ".png"  -- Path to your generated images
    local body, boundary = prepare_multipart_data(file_path)

    local headers = {
        ["Content-Type"] = "multipart/form-data; boundary=" .. boundary,
        ["Content-Length"] = tostring(#body)
    }

    return wrk.format("PUT", "/upload?lifespan=0", headers, body)
end

-- Handle the response
response = function(status, headers, body)
    if status ~= 200 then
        print("Error: Response status: " .. status)
        print("Response snippet: " .. string.sub(body, 1, 100))
    else
        print("Upload successful")
    end
end


