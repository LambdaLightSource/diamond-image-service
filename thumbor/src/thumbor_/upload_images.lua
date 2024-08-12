function read_file(file)
    local f, err = io.open(file, "rb")
    if f == nil then
        print("Error opening file: " .. err)
    end
    local content = f:read("*all")
    f:close()
    return content
end

request = function()
    local image_num = math.random(0, 999) 
    local path = "/upload"
    local file_path = "/generated_images/random_image_" .. string.format("%06d", image_num) .. ".png"
    local body = read_file(file_path)
    if body == nil then
        return wrk.format(nil, path) 
    end
    local headers = {}
    headers["Content-Type"] = "image/png" 
    
    return wrk.format("POST", path, headers, body)
end
