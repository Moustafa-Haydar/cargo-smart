<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\Role;
use Illuminate\Http\Request;
use App\Traits\ResponseTrait;

class RoleController extends Controller
{
    use ResponseTrait;

    public function addUser(StoreRoleRequest $request)
    {
        $user = UserService::addUser($request);
        return $this->responseJSON($user);
    }

    public function getAllUsers($id = null)
    {
        $users = UserService::getAllUsers($id);
        return $this->responseJSON($users);
    }

}
