<?php
namespace App\Services\Admin;
use App\Models\Role;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;
use App\Http\Requests\StoreUserRequest;

class RoleService
{
    public static function addRole(Request $request)
    {
        $data = $request->validated();
        $role = Role::create($data);
        return ($role);
    }

}