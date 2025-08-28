<?php
namespace App\Http\Controllers\Admin;
use App\Http\Controllers\Controller;
use App\Services\Admin\UserService;
use App\Http\Requests\StoreUserRequest;
use Illuminate\Http\Request;
use App\Traits\ResponseTrait;

class UserController extends Controller
{
    use ResponseTrait;

    public function getAllUsers($id = null)
    {
        $users = UserService::getAllUsers($id);
        return $this->responseJSON($users);
    }

    public function addUser(StoreUserRequest $request)
    {
        $user = UserService::addUser($request);
        return $this->responseJSON($user);
    }

    public function deleteAllUsers($id = null)
    {
        $users = UserService::deleteAllUsers($id);
        return $this->responseJSON($users);
    }

}