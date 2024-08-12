function read_file(file)
    local f = io.open(file, "rb")
    local content = f:read("*all")
    f:close()
    return content
end

request = function()
    local image_num = math.random(0, 999)
    local path = "/upload"
    local body = read_file("/generated_images/random_image_" .. string.format("%06d", image_num) .. ".png")
    local headers = {}
    headers["Content-Type"] = "application/octet-stream"
    return wrk.format("POST", path, headers, body)
end
