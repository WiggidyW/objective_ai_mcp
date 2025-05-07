python -m grpc_tools.protoc `
    --proto_path=./objective_ai_proto `
    --python_out=./proto `
    --grpc_python_out=./proto `
    --pyi_out=./proto `
    ./objective_ai_proto/objective_ai.proto